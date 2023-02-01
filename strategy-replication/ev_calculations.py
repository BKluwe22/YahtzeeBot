import numpy as np 
import itertools 
import ev_scoring as scoring
import pickle
import ray
from typing import List, Tuple
import copy 


DICE = [1,2,3,4,5,6]
CATEGORIES = ["ones", "twos", "threes", "fours", "fives", "sixes",
              "three-of-a-kind", "four-of-a-kind", "full-house",
              "small-straight", "large-straight", "yahtzee",
              "chance"]

BLOCK_1_CATEGORIES = [ "ones", "twos", "threes", "fours", "fives", "sixes" ]

BLOCK_2_CATEGORIES = [ "three-of-a-kind", "four-of-a-kind", "full-house",
                       "small-straight", "large-straight", "yahtzee",
                       "chance" ]

SUPER_YAHTZEE_CANDIDATES = [
    "three-of-a-kind", "four-of-a-kind", "full-house",
    "small-straight", "large-straight",
    "chance"  
]




def get_all_roll_outcomes() -> List[Tuple[int, int, int, int, int]]:
    """
    Generate a list of all possible outcomes of rolling five dice.

    This function generates and returns a list of tuples, each tuple 
    representing a unique outcome of rolling five dice.

    Returns:
        A list of tuples, each tuple representing a unique outcome of rolling five dice.
    """
    return list(itertools.combinations_with_replacement(DICE, r=5))


def get_all_holdouts() -> List[Tuple[int, int, int, int, int]]:
    """
    Generate a list of all possible holdouts (which dice to keep 
    and which to reroll) in the game of Yahtzee.

    This function generates and returns a list of tuples, each tuple 
    representing a unique holdout configuration in the game of Yahtzee.
    A holdout configuration is a specification of which dice to keep
    and which to reroll.

    Returns:
        A list of tuples, each tuple representing a unique holdout
        configuration in the game of Yahtzee.
    """
    
    holdouts = [list(itertools.combinations_with_replacement(DICE, r=i)) for i in range(5)]
    return list(itertools.chain(*holdouts))



def get_holdout_x_roll_probability_matrix(holdouts: List[Tuple[int, int, int, int, int]], 
                                           roll_outcomes: List[Tuple[int, int, int, int, int]]) -> np.ndarray:
    """
    Generate a matrix of probabilities representing the likelihood of 
    transitioning from each holdout to each roll outcome.

    This function takes in two lists: `holdouts` and `roll_outcomes`. 
    `holdouts` is a list of tuples representing the possible holdouts 
    in the game of Yahtzee (which dice to keep and which to reroll).
    `roll_outcomes` is a list of tuples representing the possible 
    outcomes of rolling five dice. The function generates and returns 
    a matrix of probabilities, where each element (i, j) represents the 
    probability of transitioning from the i-th holdout to the j-th roll
    outcome.

    Args:
        holdouts: A list of tuples representing the possible holdouts in the game of Yahtzee.
        roll_outcomes: A list of tuples representing the possible outcomes of rolling five dice.

    Returns:
        A matrix of probabilities, where each element (i, j) represents the 
        probability of transitioning from the i-th holdout to the j-th roll 
        outcome.
    """
    
    holdout_x_roll_probability_matrix = np.zeros((len(holdouts), len(roll_outcomes)))    
    # holdout is x-dimension
    for idx_x, holdout in enumerate(holdouts):           
        possible_next_roll_outcomes = list(itertools.combinations_with_replacement([1,2,3,4,5,6], r=5-len(holdout)))        
        possible_transitions = sorted([(holdout + t) for t in possible_next_roll_outcomes])
        # possible rolls is y-dimension, size is 252
        for idx_y, possible_roll in enumerate(roll_outcomes):            
            # Loop through all the possible transitions from holdout
            for possible_transition in possible_transitions:    
                # if a roll from the possible roll master list is equal to one 
                # of the possible transition state, then that roll is reachable
                if sorted(possible_roll) == sorted(possible_transition):                                           
                    # Quick trick to derive the next roll from the possible transition
                    # given the holdout; this is necessary to avoid looping through
                    # the next rolls from the possible_next_roll_outcomes list
                    possible_transition_l = list(possible_transition)    
                    for el in holdout: 
                        possible_transition_l.remove(el)                    
                    derived_next_roll = tuple(possible_transition_l)
                    
                    holdout_to_possible_roll_probability = np.float64(
                        len(set(itertools.permutations(derived_next_roll))) * ((1/6)**(len(derived_next_roll)))
                    )
                    
                    holdout_x_roll_probability_matrix[idx_x, idx_y] = holdout_to_possible_roll_probability
            
    return holdout_x_roll_probability_matrix 


            
def get_holdout_x_roll_probability_lookup() -> dict:
    
    """
    Generate a lookup table that maps tuples representing dice holdouts to dictionaries
    that map tuples representing dice rolls to probabilities.
    
    Returns:
        dict: A dictionary that maps tuples representing dice holdouts to dictionaries
        that map tuples representing dice rolls to probabilities.
    """
    
    holdouts = get_all_holdouts()
    roll_outcomes = get_all_roll_outcomes()
    holdout_x_roll_probability_matrix = get_holdout_x_roll_probability_matrix(holdouts,
                                                                              roll_outcomes)    
    
    holdout_x_roll_probability_lookup = {}
    for idx_x, holdout in enumerate(holdouts):
        
        holdout_x_roll_probability_lookup[holdout] = {}
        for idx_y, roll in enumerate(roll_outcomes):
            holdout_x_roll_probability_lookup[holdout][roll] = holdout_x_roll_probability_matrix[idx_x, idx_y]
            
    return holdout_x_roll_probability_lookup




def gen_empty_qtable() -> dict: 

    """
    Generate an empty Q-table table for the second block of the game. The Q-table has states as keys
    and actions as values. States are represented as tuples of form (dice, rolls_left), where dice is a tuple of the 
    current dice and rolls_left is an integer representing the number of rolls left in the current turn. Actions are 
    represented as holdouts, which are tuples of dice to keep. The function only includes holdouts that are valid for 
    the given category as actions. 

    Returns:
        dict: An empty Q-table with states as keys and actions as values.
    """
    
    rolls = get_all_roll_outcomes()
    states = [(dice, rolls_left) for dice in rolls for rolls_left in range(0, 3)]
    state_actions = {}
    for state in states: 
                
        dice, rolls_left = state
        
        if rolls_left == 0:
            state_actions[state] = [ "END" ]
        
        else: 
            valid_holdouts = []
            for i in range(len(dice)):
                valid_holdouts.append(
                    list(set(itertools.combinations(dice, r=i)))
                )
            valid_holdouts = list(itertools.chain(*valid_holdouts))
            
            state_actions[state] = valid_holdouts + [ "END" ]
            
    qtable = { state: { a: 0 for a in actions } for state, actions in state_actions.items() }
    return qtable 


@ray.remote
def fill_category_qtable(qtable_key: tuple) -> dict:

    """
    This function generates the Q-Table for a given category and whether or not a super yahtzee is possible.
    The Q-Table is a dictionary that maps states to action-values. 
    
    Parameters:
    qtable_key: tuple
        A tuple with the category (str) and whether a super yahtzee is possible (bool).
        
    Returns:
    dict
        A Q-Table with the state-action values for the given category and super yahtzee possibility.
    """

    category, super_yahtzee_possible = qtable_key
    
    if super_yahtzee_possible == True: 
        scores = { "yahtzee": 50 }
    else: 
        scores = { "yahtzee": 0 }
        
    qtable = gen_empty_qtable()
    
    pr_lookup = get_holdout_x_roll_probability_lookup()
    
    for state, actions in { k: v for k, v in qtable.items() if k[1] in [0,1] }.items() : 
        
        dice, rolls_left = state
        
        if rolls_left == 0:             
            qtable[state]["END"] = scoring.score_category(category, dice, scores)
                        
        elif rolls_left == 1: 
                         
            for action in actions.keys():
                
                if action == "END":
                    qtable[state]["END"] = scoring.score_category(category, dice, scores)
        
                else: 
                    final_roll_outcome_distribution = { k:v for k,v in pr_lookup[action].items() if v != 0 } 
                    
                    final_roll_ev_for_action = 0
                    for final_roll_outcome, final_roll_outcome_probability in final_roll_outcome_distribution.items():
                        
                        final_roll_ev_for_action += (
                            scoring.score_category(category, final_roll_outcome, scores) * final_roll_outcome_probability
                        )
        
                    qtable[state][action] = final_roll_ev_for_action
    
    
    
    for state, actions in { k: v for k, v in qtable.items() if k[1] == 2 }.items():
        
        dice, rolls_left = state
                    
        for roll_2_action in actions.keys(): 
            
            if roll_2_action == "END":
                qtable[state]["END"] = qtable[(dice, 0)]["END"] 
                
            else:                
                    
                roll_2_outcome_distribution = { k:v for k,v in pr_lookup[roll_2_action].items() if v != 0 } 
                roll_2_ev_for_action = 0
                for roll_2_outcome, roll_2_outcome_probability in roll_2_outcome_distribution.items():
                        
                    roll_2_outcome_state = qtable[(roll_2_outcome, 1)]
                    
                    best_action_roll_2 = max(roll_2_outcome_state, key=roll_2_outcome_state.get)
    
                    if best_action_roll_2 == "END":
                        roll_2_ev_for_action += (
                            qtable[(roll_2_outcome, 1)]["END"] * roll_2_outcome_probability
                        )
                        
                    else:                             
                        final_roll_outcome_distribution = { k:v for k,v in pr_lookup[best_action_roll_2].items() if v != 0 } 
                        final_roll_ev_for_action = 0
                        
                        for final_roll_outcome, final_roll_outcome_probability in final_roll_outcome_distribution.items():
                            
                            final_roll_ev_for_action += (
                                qtable[(final_roll_outcome, 0)]["END"] * final_roll_outcome_probability
                            )
                            
                        roll_2_ev_for_action += (final_roll_ev_for_action * roll_2_outcome_probability)  
                        
                qtable[state][roll_2_action] = roll_2_ev_for_action 
    

    return qtable



def round_qtables():
    
    """
    Fills the Q-tables for all categories in the game of Yahtzee.

    Returns:
        dict: A dictionary representing the Q-tables for all categories,
            with the structure {state: {qtable_key: action_values}}.
            The `state` is a tuple of (dice, rolls_left), where `dice` is
            a tuple of integers representing the current dice roll and
            `rolls_left` is an integer representing the number of rolls left.
            The `qtable_key` is a tuple of (category, super_yahtzee_possible),
            where `category` is a string representing the name of the category
            and `super_yahtzee_possible` is a boolean indicating whether
            a "super yahtzee" (rolling five of a kind) is possible in this category.
            The `action_values` is a dictionary mapping action names to their
            corresponding values.
    """
    
    qtable = {(dice, rolls_left): {} for dice in get_all_roll_outcomes() for rolls_left in range(3)}    
    for state in qtable.keys():        
        
        for category in CATEGORIES:        
            if category in SUPER_YAHTZEE_CANDIDATES:   
                
                qtable[state][(category, True)] = {}
                qtable[state][(category, False)] = {}
            
            else:             
                qtable[state][(category, None)] = {}      
    
    qtable_keys = []
    for category in CATEGORIES:        
        if category in SUPER_YAHTZEE_CANDIDATES:   
            qtable_keys.append((category, True))
            qtable_keys.append((category, False))
        else: 
            qtable_keys.append((category, None))
            
    qtables_for_category_futures = [ fill_category_qtable.remote(qtable_key) for qtable_key in qtable_keys ] 
    
    qtables_for_categories = dict(zip(qtable_keys, ray.get(qtables_for_category_futures)))
    
    for qtable_key in qtable_keys:         
        qtable_for_category = qtables_for_categories[qtable_key]
        for state, action_values in qtable_for_category.items(): 
            qtable[state][qtable_key] = action_values
                
    with open('round-qtable.pckl', 'wb') as f: 
        pickle.dump(qtable, f)
    
    return qtable



def relative_ev_qtables(): 
    """
    This function calculates the expected value of each possible strategy in the 
    current round of a game of Yahtzee. The strategies are defined as the 
    combinations of target category and whether or not a "super Yahtzee" 
    is possible in that round. The expected value of each strategy is 
    calculated by summing the expected value of each possible outcome of the 
    first roll of the round, weighted by the probability of each outcome occurring.
    The expected value of each outcome is then calculated as the highest expected 
    value achievable from the available actions in the following two rolls, 
    given the strategy being evaluated.
    
    Returns:
        dict: A dictionary with the target strategy tuples as keys and the expected value as values.

    """
    
    
    with open('round-qtable.pckl', 'rb') as f: 
        qtable = pickle.load(f)

    round_ev_for_target_strategy = {}
    for category in CATEGORIES: 
        if category in SUPER_YAHTZEE_CANDIDATES: 
            round_ev_for_target_strategy[(category, True)] = 0
            round_ev_for_target_strategy[(category, False)] = 0
        else: 
            round_ev_for_target_strategy[(category, None)] = 0
        
    empty_roll_pr_distribution = get_holdout_x_roll_probability_lookup()[()]    
    for target in round_ev_for_target_strategy.keys():     
            target_ev = 0 
            for r1_outcome, r1_probability in empty_roll_pr_distribution.items():
                qvalues_for_outcome = qtable[(r1_outcome, 2)][target]
                highest_qvalue = max(qvalues_for_outcome.values())
                target_ev += ( highest_qvalue * r1_probability )
                
            round_ev_for_target_strategy[target] = target_ev 
            
  
    with open('round-evs.pckl', 'wb') as f2:
        pickle.dump(round_ev_for_target_strategy, f2)
    
    return round_ev_for_target_strategy



def exponentiated_relative_ev_table(): 
    
    with open('round-qtable.pckl', 'rb') as f: 
        partial_q_table = pickle.load(f)
    
    with open('round-evs.pckl', 'rb') as f2:
        round_evs = pickle.load(f2)
        
    decision_table = copy.deepcopy(partial_q_table)
    
    for state, qa_values in decision_table.items():     
        for target in round_evs.keys():     
            for action in decision_table[state][target].keys():            
                qvalue_for_target = decision_table[state][target][action]
                decision_table[state][target][action] = np.exp(0.5 * ( qvalue_for_target - round_evs[target] ))
    
    with open('decision-qtable.pckl', 'wb') as f2: 
        pickle.dump(decision_table, f2)
        
    return decision_table





def build_tables(): 
    
    round_qtables()
    relative_ev_qtables()
    exponentiated_relative_ev_table()






