import itertools 
from collections import Counter
from typing import Union



def ones_value(roll_result: tuple, scores: dict) -> Union[int, float]:
    """
    Calculate the bonus-adjusted expected value of a given roll of dice 
    for the "ones" category in the game of Yahtzee.
    
    This function takes in a tuple of integers, roll_result, representing 
    the result of rolling five dice, and a dictionary, scores, representing
    the current scores for all categories in the game. The bonus-adjusted 
    expected value of the roll for the "ones" category is calculated based 
    on the number of 1s in roll_result, with additional bonuses applied
    for rolling more than three 1s.
    
    Args:
    roll_result: A tuple of integers representing the result of rolling five dice.
    scores: A dictionary representing the current scores for all categories in the game.
    
    Returns:
    An integer or float representing the bonus-adjusted expected value of 
    the roll for the "ones" category.
    """
    n = 1
    n_count = roll_result.count(n)
    raw_value = n_count*n     
 
    if n_count == 3:
        return raw_value + (raw_value*35)/63
    elif n_count >= 4:
        return raw_value + ((raw_value*35)/63) + ((n*35)/21)
    else: 
        return raw_value
    
    
def twos_value(roll_result: tuple, scores: dict) -> Union[int, float]:
    """
    Calculate the bonus-adjusted expected value of a given roll of dice for
    the "twos" category in the game of Yahtzee.
    
    This function takes in a tuple of integers, roll_result, representing the 
    result of rolling five dice, and a dictionary, scores, representing the 
    current scores for all categories in the game. The bonus-adjusted expected
    value of the roll for the "twos" category is calculated based on the number
    of 2s in roll_result, with additional bonuses applied for rolling more than
    three 2s.
    
    Args:
    roll_result: A tuple of integers representing the result of rolling five dice.
    scores: A dictionary representing the current scores for all categories in the game.
    
    Returns:
    An integer or float representing the bonus-adjusted expected value of the 
    roll for the "twos" category.
    """
    
    n = 2
    n_count = roll_result.count(n)
    raw_value = n_count*n     
    
    if n_count == 3:
        return raw_value + (raw_value*35)/63
    elif n_count >= 4:
        return raw_value + ((raw_value*35)/63) + ((n*35)/21)
    else: 
        return raw_value
    

def threes_value(roll_result: tuple, scores: dict) -> Union[int, float]:
    """
    Calculate the bonus-adjusted expected value of a given roll of dice for
    the "threes" category in the game of Yahtzee.
    
    This function takes in a tuple of integers, roll_result, representing the 
    result of rolling five dice, and a dictionary, scores, representing the 
    current scores for all categories in the game. The bonus-adjusted expected
    value of the roll for the "threes" category is calculated based on the number
    of 3s in roll_result, with additional bonuses applied for rolling more than
    three 3s.
    
    Args:
    roll_result: A tuple of integers representing the result of rolling five dice.
    scores: A dictionary representing the current scores for all categories in the game.
    
    Returns:
    An integer or float representing the bonus-adjusted expected value of the 
    roll for the "threes" category.
    """
    
    n = 3
    n_count = roll_result.count(n)
    raw_value = n_count*n     
    
    if n_count == 3:
        return raw_value + (raw_value*35)/63
    elif n_count >= 4:
        return raw_value + ((raw_value*35)/63) + ((n*35)/21)
    else: 
        return raw_value
    
    
def fours_value(roll_result: tuple, scores: dict) -> Union[int, float]:
    """
    Calculate the bonus-adjusted expected value of a given roll of dice for
    the "fours" category in the game of Yahtzee.
    
    This function takes in a tuple of integers, roll_result, representing the 
    result of rolling five dice, and a dictionary, scores, representing the 
    current scores for all categories in the game. The bonus-adjusted expected
    value of the roll for the "fours" category is calculated based on the number
    of 4s in roll_result, with additional bonuses applied for rolling more than
    three 4s.
    
    Args:
    roll_result: A tuple of integers representing the result of rolling five dice.
    scores: A dictionary representing the current scores for all categories in the game.
    
    Returns:
    An integer or float representing the bonus-adjusted expected value of the 
    roll for the "fours" category.
    """
    
    n = 4
    n_count = roll_result.count(n)
    raw_value = n_count*n     
    
    if n_count == 3:
        return raw_value + (raw_value*35)/63
    elif n_count >= 4:
        return raw_value + ((raw_value*35)/63) + ((n*35)/21)
    else: 
        return raw_value

    

def fives_value(roll_result: tuple, scores: dict) -> Union[int, float]:
    """
    Calculate the bonus-adjusted expected value of a given roll of dice for
    the "fives" category in the game of Yahtzee.
    
    This function takes in a tuple of integers, roll_result, representing the 
    result of rolling five dice, and a dictionary, scores, representing the 
    current scores for all categories in the game. The bonus-adjusted expected
    value of the roll for the "fives" category is calculated based on the number
    of 5s in roll_result, with additional bonuses applied for rolling more than
    three 5s.
    
    Args:
    roll_result: A tuple of integers representing the result of rolling five dice.
    scores: A dictionary representing the current scores for all categories in the game.
    
    Returns:
    An integer or float representing the bonus-adjusted expected value of the 
    roll for the "fives" category.
    """
    
    n = 5
    n_count = roll_result.count(n)
    raw_value = n_count*n     
    
    if n_count == 3:
        return raw_value + (raw_value*35)/63
    elif n_count >= 4:
        return raw_value + ((raw_value*35)/63) + ((n*35)/21)
    else: 
        return raw_value
    

def sixes_value(roll_result: tuple, scores: dict) -> Union[int, float]:
    """
    Calculate the bonus-adjusted expected value of a given roll of dice for
    the "sixes" category in the game of Yahtzee.
    
    This function takes in a tuple of integers, roll_result, representing the 
    result of rolling five dice, and a dictionary, scores, representing the 
    current scores for all categories in the game. The bonus-adjusted expected
    value of the roll for the "sixes" category is calculated based on the number
    of 6s in roll_result, with additional bonuses applied for rolling more than
    three 6s.
    
    Args:
    roll_result: A tuple of integers representing the result of rolling five dice.
    scores: A dictionary representing the current scores for all categories in the game.
    
    Returns:
    An integer or float representing the bonus-adjusted expected value of the 
    roll for the "sixes" category.
    """
    
    n = 6
    n_count = roll_result.count(n)
    raw_value = n_count*n     
    
    if n_count == 3:
        return raw_value + (raw_value*35)/63
    elif n_count >= 4:
        return raw_value + ((raw_value*35)/63) + ((n*35)/21)
    else: 
        return raw_value


def three_of_a_kind_value(roll_result: tuple, scores: dict) -> int:   
    """
    Calculate the value of a given roll of dice for the "three of a kind" 
    category in the game of Yahtzee.
    
    This function takes in a tuple of integers, roll_result, representing the 
    result of rolling five dice, and a dictionary, scores, representing the
    current scores for all categories in the game. The value of the roll for 
    the "three of a kind" category is calculated based on the number of dice
    with the same value in roll_result, with additional bonuses applied for 
    rolling a "yahtzee" (all five dice showing the same value) or a "super yahtzee"
    (rolling a yahtzee and already having a score of 50 in the "yahtzee" category).
    
    Args:
    roll_result: A tuple of integers representing the result of rolling five dice.
    scores: A dictionary representing the current scores for all categories in the game.
    
    Returns:
    An integer representing the value of the roll for the "three of a kind" category.
    """
    
    modal_dice = Counter(roll_result).most_common(1)

    # If highest n rolled dice is less than 3, the score will be zero
    if modal_dice[0][1] < 3: 
        return 0
   
    else: 
        
        # If all 5 dice are the same
        if all(x == roll_result[0] for x in roll_result):
           
            # SUPER YAHTZEE EDGE CASE
            if scores["yahtzee"] == 50: 
                return 100
           
            else:
                return sum(roll_result)
           
        else: 
            return sum(roll_result)
               
       
        
def four_of_a_kind_value(roll_result: tuple, scores: dict) -> int:   
    """
    Calculate the value of a given roll of dice for the "four of a kind" 
    category in the game of Yahtzee.
    
    This function takes in a tuple of integers, roll_result, representing the 
    result of rolling five dice, and a dictionary, scores, representing the
    current scores for all categories in the game. The value of the roll for 
    the "three of a kind" category is calculated based on the number of dice
    with the same value in roll_result, with additional bonuses applied for 
    rolling a "yahtzee" (all five dice showing the same value) or a "super yahtzee"
    (rolling a yahtzee and already having a score of 50 in the "yahtzee" category).
    
    Args:
    roll_result: A tuple of integers representing the result of rolling five dice.
    scores: A dictionary representing the current scores for all categories in the game.
    
    Returns:
    An integer representing the value of the roll for the "four of a kind" category.
    """
    
    modal_dice = Counter(roll_result).most_common(1)

    # If highest n rolled dice is less than 3, the score will be zero
    if modal_dice[0][1] < 4: 
        return 0
   
    else: 
        
        # If all 5 dice are the same
        if all(x == roll_result[0] for x in roll_result):
           
            # SUPER YAHTZEE EDGE CASE
            if scores["yahtzee"] == 50: 
                return 100
           
            else:
                return sum(roll_result)
           
        else: 
            return sum(roll_result)
        
        
    
    
def full_house_value(roll_result: tuple, scores: dict) -> int:
    """
    Calculate the value of a given roll of dice for the "full house" 
    category in the game of Yahtzee.
    
    This function takes in a tuple of integers, roll_result, representing
    the result of rolling five dice, and a dictionary, scores, representing 
    the current scores for all categories in the game. The value of the roll 
    for the "full house" category is calculated based on whether roll_result 
    contains a full house (a pair and a three of a kind). If roll_result is a
    "super yahtzee" (all five dice showing the same value and the "yahtzee"
    category already having a score of 50), the return value is 100.
    
    Args:
    roll_result: A tuple of integers representing the result of rolling five dice.
    scores: A dictionary representing the current scores for all categories in the game.
    
    Returns:
    An integer representing the value of the roll for the "full house" category.
    If the roll is a full house, the return value is 25. If the roll is a
    "super yahtzee", the return value is 100. Otherwise, the return value is 0.
    """
    
    top_two_dice = Counter(roll_result).most_common(2)

    # SUPER YAHTZEE EDGE CASE
    if all(x == roll_result[0] for x in roll_result):
       
        # SUPER YAHTZEE EDGE CASE
        if scores["yahtzee"] == 50: 
            return 100
       
        else:
            return 0
            
    else: 
        
        if top_two_dice[0][1] == 3 and top_two_dice[1][1] == 2:
            return 25 
        
        else: 
            return 0
        
        
        
def small_straight_value(roll_result: tuple, scores: dict) -> int:    
    """
    Calculate the value of a given roll of dice for the "small straight"
    category in the game of Yahtzee.
    
    This function takes in a tuple of integers, roll_result, representing 
    the result of rolling five dice, and a dictionary, scores, representing
    the current scores for all categories in the game. The value of the roll 
    for the "small straight" category is calculated based on whether roll_result
    contains a small straight (four dice showing a consecutive sequence of values).
    If roll_result is a "super yahtzee" (all five dice showing the same value 
    and the "yahtzee" category already having a score of 50), the return value is 100.
    
    Args:
    roll_result: A tuple of integers representing the result of rolling five dice.
    scores: A dictionary representing the current scores for all categories in the game.
    
    Returns:
    An integer representing the value of the roll for the "small straight" category. 
    If the roll is a small straight, the return value is 30. If the roll is a 
    "super yahtzee", the return value is 100. Otherwise, the return value is 0.
    """
    # SUPER YAHTZEE EDGE CASE
    if all(x == roll_result[0] for x in roll_result):
       
        # SUPER YAHTZEE EDGE CASE
        if scores["yahtzee"] == 50: 
            return 100
       
        else:
            return 0
                        
    else:
        
        valid_small_streets = [
            [1,2,3,4,5],
            [2,3,4,5,6],        
            [1,2,3,4],
            [2,3,4,5],
            [3,4,5,6],         
        ]
        
        roll_result_sub_streets = [sorted(x) for x in list(itertools.combinations(roll_result, r=4))]
        
        for candidate_combo in roll_result_sub_streets:
            for ks in valid_small_streets: 
                if candidate_combo == ks: 
                    return 30
        else: 
            return 0         
    
    
    
def large_straight_value(roll_result: tuple, scores: dict) -> int:    
    """
    Calculate the value of a given roll of dice for the "large straight"
    category in the game of Yahtzee.
    
    This function takes in a tuple of integers, roll_result, representing the 
    result of rolling five dice, and a dictionary, scores, representing the 
    current scores for all categories in the game. The value of the roll for the 
    "large straight" category is calculated based on whether roll_result contains 
    a large straight (five dice showing a consecutive sequence of values). 
    If roll_result is a "super yahtzee" (all five dice showing the same value
    and the "yahtzee" category already having a score of 50), the return value is 100.
    
    Args:
    roll_result: A tuple of integers representing the result of rolling five dice.
    scores: A dictionary representing the current scores for all categories in the game.
    
    Returns:
    An integer representing the value of the roll for the "large straight" 
    category. If the roll is a large straight, the return value is 40. If the 
    roll is a "super yahtzee", the return value is 100. Otherwise, 
    the return value is 0.
    """
    # SUPER YAHTZEE EDGE CASE
    if all(x == roll_result[0] for x in roll_result):
       
        # SUPER YAHTZEE EDGE CASE
        if scores["yahtzee"] == 50: 
            return 100
       
        else:
            return 0
                        
    else:
        
        valid_large_streets = [
            [1,2,3,4,5],
            [2,3,4,5,6],   
        ]
        
        if list(roll_result) in valid_large_streets:
            return 40
        else: 
            return 0
    
    
    
def yahtzee_value(roll_result: tuple, scores: dict) -> int:    
    """
    Calculate the value of a given roll of dice for the "yahtzee" 
    category in the game of Yahtzee.
    
    This function takes in a tuple of integers, roll_result, representing 
    the result of rolling five dice, and a dictionary, scores, representing 
    the current scores for all categories in the game. The value of the roll 
    for the "yahtzee" category is calculated based on whether roll_result 
    contains a yahtzee (all five dice showing the same value).
    
    Args:
    roll_result: A tuple of integers representing the result of rolling five dice.
    scores: A dictionary representing the current scores for all categories in the game.
    
    Returns:
    An integer representing the value of the roll for the "yahtzee" category. 
    If the roll is a yahtzee, the return value is 50. Otherwise, the return
    value is 0.
    """
    
    if all(roll_result[0] == x for x in roll_result):
        return 50
    else:
        return 0
    
    
    
def chance_value(roll_result: tuple, scores: dict) -> int:    
    
    """
    Calculate the value of a given roll of dice for the "chance" category
    in the game of Yahtzee.
    
    This function takes in a tuple of integers, roll_result, representing
    the result of rolling five dice, and a dictionary, scores, representing 
    the current scores for all categories in the game. The value of the roll 
    for the "chance" category is calculated by summing the values of all dice
    in roll_result. If roll_result is a "super yahtzee" (all five dice showing 
    the same value and the "yahtzee" category already having a score of 50), 
    the return value is 100.
    
    Args:
    roll_result: A tuple of integers representing the result of rolling five dice.
    scores: A dictionary representing the current scores for all categories in the game.
    
    Returns:
    An integer representing the value of the roll for the "chance" category. 
    If the roll is a "super yahtzee", the return value is 100. Otherwise, the
    return value is the sum of the values of all dice in roll_result.
    """

    # SUPER YAHTZEE EDGE CASE
    if all(x == roll_result[0] for x in roll_result):           
        if scores["yahtzee"] == 50: 
                return 100
        else:
            return sum(roll_result) 
    else:            
        return sum(roll_result)    
       
        
        
def score_category(category: str, roll_result: tuple, scores: dict) -> Union[int, float]:
    
    """
    Calculate the expected value of a given roll of dice for a specified 
    category in the game of Yahtzee.
    
    This function takes in a string, category, representing the category 
    for which to calculate the score, a tuple of integers, roll_result, 
    representing the result of rolling five dice, and a dictionary, scores,
    representing the current scores for all categories in the game. The 
    expected value of the roll for the specified category is calculated by 
    calling the appropriate scoring function based on the value of category.
    For categories "ones", "twos", "threes", "fours", "fives", and "sixes",
    the expected value is calculated as the bonus-adjusted expected value.
    
    Args:
        
    category: A string representing the category for which to calculate the score. 
    Must be one of the following: "ones", "twos", "threes", "fours", "fives", "sixes", 
    "three-of-a-kind", "four-of-a-kind", "full-house", "small-straight", "large-straight", 
    "yahtzee", "chance".
    
    roll_result: A tuple of integers representing the result of rolling five dice.
    scores: A dictionary representing the current scores for all categories in the game.
    
    Returns:
    An integer or float representing the expected value for the category given the
    roll_result and scores.
    """
    
    target_scoring_func_mapping = {
        "ones": ones_value,
        "twos": twos_value,
        "threes": threes_value,
        "fours": fours_value,
        "fives": fives_value,
        "sixes": sixes_value,
        
        "three-of-a-kind": three_of_a_kind_value,
        "four-of-a-kind": four_of_a_kind_value,
        "full-house": full_house_value,
        "small-straight": small_straight_value,
        "large-straight": large_straight_value,
        "yahtzee": yahtzee_value,
        "chance": chance_value        
    }
    
    return target_scoring_func_mapping[category](roll_result, scores)
    





        
        
        
        