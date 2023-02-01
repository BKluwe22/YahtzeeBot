import numpy as np 
import true_scoring as scoring
import copy

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
        self._fills = { cat: False for cat in self.CATEGORIES } if fills is None else fills
        self._scores = { cat: 0 for cat in self.CATEGORIES } if scores is None else scores
        
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
            
            # if all categories are filled, this was the last decision and game
            # is over
            if all(fill == True for fill in self._fills.values()):   
                done = True                   
                
                observation = self._get_obs()
                
                # Return new state tuple
                return observation, done
        
            # finish the turn, re-roll the dice with NO HOLDOUT and set rolls_left
            # back to 2. 
            else:
                done = False

                self._dice = self._roll_dice(holdout=())
                self._rolls_left = 2                 
                
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
            
