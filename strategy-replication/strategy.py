import ray
import itertools
import copy
import numpy as np
import true_scoring as scoring
import pickle
import scipy.stats 
from typing import TypeVar, Union
import pandas as pd 
import pprint 
from pandas_profiling import ProfileReport
from collections import ChainMap, OrderedDict


YahtzeeAgent = TypeVar('YahtzeeAgent')

CATEGORIES = ["ones", "twos", "threes", "fours", "fives", "sixes",
              "three-of-a-kind", "four-of-a-kind", "full-house",
              "small-straight", "large-straight", "yahtzee",
              "chance"]

BLOCK_1_CATEGORIES = ["ones", "twos", "threes", "fours", "fives", "sixes"]
BLOCK_2_CATEGORIES = ["three-of-a-kind", "four-of-a-kind", "full-house",
                      "small-straight", "large-straight", "yahtzee",
                      "chance"]

BLOCK_1_CATGEORY_NUM_VALUE_MAP = {
    "ones": 1,
    "twos": 2, 
    "threes": 3,
    "fours": 4,
    "fives": 5,
    "sixes": 6,
}



SUPER_YAHTZEE_CANDIDATES = [
    "three-of-a-kind", "four-of-a-kind", "full-house", "small-straight",
    "large-straight", "chance"
]


@ray.remote
def simulate_branch(agent: YahtzeeAgent, 
                    num_games: int, 
                    init_state: dict, 
                    action: Union[str, tuple],
                    summary: bool) -> dict:
    
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

    if summary: 
        return {
            "action": action,
            "n_observations": len(scores),
            "mean": float(np.mean(scores)),
            "median": float(np.median(scores)),
            "min": int(np.min(scores)),
            "max": int(np.max(scores)),
            "skew": scipy.stats.skew(scores),
            "kurtosis": scipy.stats.kurtosis(scores)
        }
    
    else: 
        return {
            action: scores
        }



   
   
class YahtzeeAgent:
      
  
    def __init__(self, env):
        """
        Initialize the YahtzeeAgent with an environment and load the decision table.

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
        - n_best (int, optional): an integer representing the number of best actions to return. The default value is 1.
        
        Returns:
        - (list): a list of the n_best best actions to take, ordered from highest to lowest probability.
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
       
            
    

    def parallel_monte_carlo(self, simulations_per_branch, init_state, actions, summary):
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
            action=action,
            summary=summary
        ) for action in actions]

        return OrderedDict(ChainMap(*ray.get(simulation_futures)))


    
    def benchmark(self, n_games: int) -> dict:
        
        np.random.seed(22)
        
        games = []
        scores = []
        for g in range(n_games):
            
            state = self.env.reset()

            for r in itertools.count():
                action = self.select_action(state)

                next_state, done = self.env.step(action)
    
                state = next_state
                
                if done: 
                    game_data = { k: v for k, v in state["scores"].items() }
                    game_data.update({ "has_bonus": scoring.has_bonus(state["scores"]) })
                    game_data.update({ "block1_score": scoring.get_block_1_score(state["scores"])})
                    game_data.update({ "block2_score": scoring.get_block_2_score(state["scores"])})
                    game_data.update({ "total_score": scoring.score_game(state["scores"])})
                    
                    games.append(game_data)
                    
                    scores.append(scoring.score_game(state["scores"]))
                    break
                
            
        pprint.pprint({
            "n_observations": len(scores),
            "mean": float(np.mean(scores)),
            "median": float(np.median(scores)),
            "min": int(np.min(scores)),
            "max": int(np.max(scores)),
            "skew": scipy.stats.skew(scores),
            "kurtosis": scipy.stats.kurtosis(scores)
        })
        return pd.DataFrame(games)
    
       
    
    def strategy_benchmark_report(self, n_games: int):
        
        games = self.benchmark(n_games)
        profile = ProfileReport(games, 
                                title="Yahtzee Strategy Benchmark Report",
                                correlations=None,
                                missing_diagrams=None,
                                duplicates=None,
                                interactions=None,
                                dark_mode=True)
        
        profile.config.html.navbar_show = False

        profile.to_file("yahtzee-strategy-benchmark.html")

 
    
    
    