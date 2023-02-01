import ray
import itertools
import copy
import numpy as np
import true_scoring as scoring
import pickle
import yahtzee
from flask import Flask, request, jsonify
import scipy.stats 
from typing import TypeVar, Union

ray.init()


YahtzeeAgent = TypeVar('YahtzeeAgent')

CATEGORIES = ["ones", "twos", "threes", "fours", "fives", "sixes",
              "three-of-a-kind", "four-of-a-kind", "full-house",
              "small-straight", "large-straight", "yahtzee",
              "chance"]

BLOCK_1_CATEGORIES = ["ones", "twos", "threes", "fours", "fives", "sixes"]


SUPER_YAHTZEE_CANDIDATES = [
    "three-of-a-kind", "four-of-a-kind", "full-house", "small-straight",
    "large-straight", "chance"
]


@ray.remote
def simulate_branch(agent: YahtzeeAgent, num_games: int, init_state: dict, action: Union[str, tuple]) -> dict:
    
    """
    Simulates the game of Yahtzee for a given agent and action.
    
    Args:
    agent (YahtzeeAgent): The agent being used to play Yahtzee.
    num_games (int): The number of games to simulate.
    init_state (dict): The initial state of the game.
    action (str or tuple): The action being taken in the initial round.
    
    Returns:
    dict: A dictionary containing the action taken, number of observations, mean score, median score,
    minimum score, maximum score, skew, and kurtosis of the simulated games.
    """
    
    scores = []
    for _ in range(num_games):

        starting_state = copy.deepcopy(init_state)

        init_dice = starting_state["dice"]
        init_rolls_left = starting_state["rolls_left"]
        init_fills = { k.replace('_', '-'): v for k,v in starting_state["fills"].items() }
        init_scores = { k.replace('_', '-'): v for k,v in starting_state["scores"].items() }

        state = agent.env.reset(
            dice=tuple(init_dice),
            rolls_left=init_rolls_left,
            fills=init_fills,
            scores=init_scores
        )
        
        if isinstance(action, list):
            action = tuple(action)

        state, done = agent.env.step(action)

        for r in itertools.count():
            action_s = agent.select_action(state)
            next_state, done = agent.env.step(action_s)
            state = next_state
            if done:
                scores.append(int(scoring.score_game(state["scores"])))
                break

    return {
        "action": action,
        "scores": scores,
        "n_observations": len(scores),
        "mean": float(np.mean(scores)),
        "median": float(np.median(scores)),
        "min": int(np.min(scores)),
        "max": int(np.max(scores)),
        "skew": scipy.stats.skew(scores),
        "kurtosis": scipy.stats.kurtosis(scores)
    }


class YahtzeeAgent:

    def __init__(self, env):
        """
        Initialize the YahtzeeAgent with an environment and load the round q-table and round expected values.

        Parameters:
        env (Yahtzee): An instance of the Yahtzee class representing the environment in which the agent will interact.
        """
        
        self.env = env
        self.decision_table = self._decision_table()


    def _decision_table(self):
        """
        Load the round q-table from file and return it.

        Returns:
        dict: The round q-table.
        """
       
        with open('decision-qtable.pckl', 'rb') as f:
            decision_table = pickle.load(f)
        return decision_table
    
    
    def select_action(self, state: dict):
        
        """
        Select the best action to take in the current Yahtzee game state.
        
        Parameters:
        - state (dict): a dictionary representing the current state of the game.
        
        Returns:
        - string|tuple: the best action according to the model 
        """
        
        dice = state["dice"]
        scores = state["scores"]
        rolls_left = state["rolls_left"]
        fills = state["fills"]
        

        open_categories = [cat.replace('_', '-') for cat, fill_bool in fills.items() if fill_bool == False]

        super_yahtzee_possible = (scores["yahtzee"] == 50)

        lookup_keys = [(cat, super_yahtzee_possible) if cat in SUPER_YAHTZEE_CANDIDATES
                        else (cat, None) for cat in open_categories]

        r_decision_table = { k: v for k, v in self.decision_table[(dice, rolls_left)].items()
                              if k in lookup_keys }

        best_actions = {}
        for k, v in r_decision_table.items():

            highest_val_action_key = max(v, key=v.get)
                        
            if highest_val_action_key == "END":
                highest_val_action_key = k[0]
                
            if highest_val_action_key not in best_actions.keys():
                if isinstance(highest_val_action_key, str):                                                        
                    best_actions[highest_val_action_key] = v["END"]
                    
                else: 
                    best_actions[highest_val_action_key] = v[highest_val_action_key]
            else: 
                if isinstance(highest_val_action_key, str):
                    best_actions[highest_val_action_key] = v["END"]
                else: 
                    best_actions[highest_val_action_key] += v[highest_val_action_key]

          
        return max(best_actions, key=best_actions.get)
       

    def parallel_simulate_actions(self, simulations_per_branch, init_state, actions):
        """
        Run parallel Monte Carlo simulations for a given set of actions.

        Parameters:
        simulations_per_branch (int): The number of simulations to run per action branch.
        init_state (dict): The initial state for the simulations.
        actions (list): A list of actions to simulate.

        Returns:
        list: A list of dictionaries representing the results of the simulations.
        """
        
        simulation_futures = [simulate_branch.remote(
            agent=self,
            num_games=simulations_per_branch,
            init_state=init_state,
            action=action
        ) for action in actions]

        return ray.get(simulation_futures)



# env = yahtzee.Yahtzee()
# agent = YahtzeeAgent(env)

# init_state = {
#     "dice": (2,2,3,3,3),
#     "rolls_left": 2,
#     "scores": { cat: 0 for cat in CATEGORIES },
#     "fills": { cat: False for cat in CATEGORIES }
# }

# results = agent.parallel_simulate_actions(
#     100,
#     init_state,
#     ["full-house", (3,3,3), (2,2), (2,)]
# )

# import pandas as pd 
# test = pd.read_json(json.dumps(results))
# data = pd.DataFrame(results)

# score_df = data[['action', 'scores']]
# score_df = score_df.explode('scores').reset_index(drop=True)

# stat_df = data.drop(['action', 'scores'], axis=1)


# import plotly.express as px 

# fig = px.histogram(score_df, x='scores', 
#                    facet_col='action',
#                    facet_col_wrap=3)
# fig.write_html('scores.html')

app = Flask(__name__)

@app.route('/simulate', methods=['POST'])
def send_simulation_results():

    content = request.json

    env = yahtzee.Yahtzee()
    agent = YahtzeeAgent(env)

    init_state = {
        "dice": tuple(content["dice"]),
        "rolls_left": content["rolls_left"],
        "scores": content["scores"],
        "fills": content["fills"]
    }

    results = agent.parallel_simulate_actions(
        content["n_simulations"],
        init_state,
        content["simulation_actions"]
    )

    return jsonify(results)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
