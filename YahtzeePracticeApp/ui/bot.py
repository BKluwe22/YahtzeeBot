import itertools
import copy
import numpy as np
import true_scoring as scoring
import pickle
from collections import OrderedDict



CATEGORIES = ["ones", "twos", "threes", "fours", "fives", "sixes",
              "three-of-a-kind", "four-of-a-kind", "full-house",
              "small-straight", "large-straight", "yahtzee",
              "chance"]

BLOCK_1_CATEGORIES = ["ones", "twos", "threes", "fours", "fives", "sixes"]

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



class Yahtzee:
    """
    Yahtzee game class. Initializes game with standard dice rolling and scoring rules. 
    
    Parameters
    ----------
    dice : tuple, optional
        Tuple of 5 integers representing the current dice roll.
    rolls_left : int, optional
        Number of rolls left in the current turn.
    fills : dict, optional
        Dictionary indicating whether each category has been filled.
    scores : dict, optional
        Dictionary of current scores for each category.
    
    Attributes
    ----------
    CATEGORIES : list
        List of available categories for scoring.
    _dice : tuple
        Tuple of 5 integers representing the current dice roll.
    _rolls_left : int
        Number of rolls left in the current turn.
    _fills : dict
        Dictionary indicating whether each category has been filled.
    _scores : dict
        Dictionary of current scores for each category.
    
    Methods
    -------
    reset(self, dice=None, rolls_left=None, fills=None, scores=None) -> dict
        Reset game to initial state.
    step(self, action) -> tuple
        Take a step in the game based on a given action.
    """
    
    def __init__(self):        
        
        self.CATEGORIES = ["ones", "twos", "threes", "fours", "fives", "sixes",
                           "three-of-a-kind", "four-of-a-kind", "full-house",
                           "small-straight", "large-straight", "yahtzee",
                           "chance"]
        

    def _roll_dice(self, holdout: tuple = ()) -> tuple: 
        """
        Roll the dice in the Yahtzee game.
        
        Parameters:
        - holdout (tuple): a tuple of integers representing the dice that should not be re-rolled.
        
        Returns:
        - (tuple): a tuple of integers representing the result of the dice roll.
        """
        
        rolled_dice = ()
        for _ in range(5-len(holdout)):
            rolled_dice += (np.random.choice(a=[1,2,3,4,5,6]), )
        
        return tuple(sorted(rolled_dice + holdout))
    
    
    def _get_obs(self):
        """
        Get the observation for the current state of the Yahtzee game.
        
        Returns:
        - (dict): a dictionary representing the current state of the game.
        """
        
        return {
            "dice": self._dice,
            "rolls_left": self._rolls_left, 
            "fills": copy.deepcopy( self._fills ),
            "scores": copy.deepcopy( self._scores ), 
        }
        
    
    def reset(self, dice=None, rolls_left=None, fills=None, scores=None):
        """
        Reset the Yahtzee game.
        
        Parameters:
        - dice (tuple): a tuple of integers representing the result of the dice roll (optional).
        - rolls_left (int): the number of rolls left for the player (optional).
        - fills (dict): a dictionary representing the categories that have already been filled (optional).
        - scores (dict): a dictionary representing the scores for each category (optional).
        
        Returns:
        - (dict): a dictionary representing the initial state of the game.
        """            
        
        self._dice = self._roll_dice(holdout=()) if dice is None else dice
        self._rolls_left = 2 if rolls_left is None else rolls_left
        self._fills = OrderedDict({ cat: False for cat in self.CATEGORIES }) if fills is None else fills
        self._scores = OrderedDict({ cat: 0 for cat in self.CATEGORIES }) if scores is None else scores
        
        observation = self._get_obs()

        return observation
    

    def step(self, action):
        """
        Take a step in the Yahtzee game.
        
        Parameters:
        - action (str or tuple): a string representing the chosen category or a tuple of integers representing the dice to hold.
        
        Returns:
        - (tuple): a tuple containing the observation for the new state of the game and a boolean indicating if the game is done.
        """
        
        # if decision is a category
        if isinstance(action, str):
                        
            score = scoring.score_category(action, self._dice, self._scores)
            
            self._scores[action] = score
            self._fills[action] = True
            
            done = True 
            observation = self._get_obs()
            
            return observation, done 
            
        # decision is a tuple -> agent decides to re-roll. Decrement the rolls_left 
        # parameter, no change to fills or scores, reward is zero
        else: 
            done = False
            
            self._dice = self._roll_dice(holdout=action)
            self._rolls_left = self._rolls_left - 1            
            
            observation = self._get_obs()
            
            return observation, done
            





class YahtzeeBot:
    
  
    def __init__(self):
        """
        Initialize the YahtzeeAgent with an environment and load the round q-table and round expected values.

        Parameters:
        env (Yahtzee): An instance of the Yahtzee class representing the environment in which the agent will interact.
        """
        
        self.env = Yahtzee()
        self.round_qtable = self._round_qtable()
        self.round_evs = self._round_evs()

    def _round_qtable(self):
        """
        Load the round q-table from file and return it.

        Returns:
        dict: The round q-table.
       """
       
        with open('round-qtable.pckl', 'rb') as f:
            round_qtable = pickle.load(f)
        return round_qtable

    def _round_evs(self):
        
        """
        Load the round expected values from file and return them.

        Returns:
        dict: The round expected values.
        """
        
        with open('round-evs.pckl', 'rb') as f:
            round_evs = pickle.load(f)
        return round_evs
    

    def select_action(self, state):
            
        dice = state["dice"]
        scores = state["scores"]
        rolls_left = state["rolls_left"]
        fills = state["fills"]
        
        open_categories = [ cat.replace('_', '-') for cat, fill_bool in fills.items() if fill_bool == False ]
                                
        super_yahtzee_possible = ( scores["yahtzee"] == 50 )
        
        lookup_keys = [ (cat, super_yahtzee_possible) if cat in SUPER_YAHTZEE_CANDIDATES 
                        else (cat, None) for cat in open_categories ]
            
        r_qtable = { k: v for k, v in self.round_qtable[(dice, rolls_left)].items()
                                     if k in lookup_keys }
                
        best_actions = {}
        exp_best_actions = {}

        for k, v in r_qtable.items(): 

            highest_value_relative_value_action_key = (max(v, key=v.get))
            
            highest_relative_value = v[highest_value_relative_value_action_key] - self.round_evs[k]
            exp_highest_relative_value = np.exp(0.5*highest_relative_value)
                   
            if (k[0], highest_value_relative_value_action_key) not in best_actions.keys():
                best_actions[(k[0], highest_value_relative_value_action_key)] = highest_relative_value
          
            else: 
                best_actions[(k[0], highest_value_relative_value_action_key)] += highest_relative_value
      
            if highest_value_relative_value_action_key == "END":
                highest_value_relative_value_action_key = k[0]
                
            if highest_value_relative_value_action_key not in exp_best_actions.keys():
                exp_best_actions[highest_value_relative_value_action_key] = exp_highest_relative_value
                
            else: 
                exp_best_actions[highest_value_relative_value_action_key] += exp_highest_relative_value

        return best_actions, exp_best_actions, max(exp_best_actions, key = exp_best_actions.get)



    
    def play_turn(self, fills, scores):
        
        turn_steps = []
        turn_results = {}
        
        state = self.env.reset(dice=None, rolls_left=None, fills=fills, scores=scores)
        
        for turn in itertools.count(): 
            
            relative_action_values, exp_action_values, action = self.select_action(state)

            turn_steps.append({
                "state": state,
                "action": action,
                "action_ranking": exp_action_values,
                "relative_action_values": relative_action_values
            })

            next_state, done = self.env.step(action)

            state = next_state
            
            if done: 
                turn_results["fills"] = state["fills"]
                turn_results["scores"] = state["scores"]
                break
        
        return turn_steps, turn_results
                

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    