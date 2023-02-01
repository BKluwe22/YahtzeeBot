import itertools 
from collections import Counter



def ones_value(roll_result, scores):
    """
    Calculate the score for the 'Ones' category in Yahtzee.
    
    Parameters:
    - roll_result (list): a list of integers representing the face values of the dice.
    - scores (dict): a dictionary representing the scores for each category.
    
    Returns:
    - (int): the score for the 'Ones' category.
    """
    
    raw_score = roll_result.count(1)*1
    return raw_score
    
    
def twos_value(roll_result, scores): 
    """
    Calculate the score for the 'Twos' category in Yahtzee.
    
    Parameters:
    - roll_result (list): a list of integers representing the face values of the dice.
    - scores (dict): a dictionary representing the scores for each category.
    
    Returns:
    - (int): the score for the 'Twos' category.
    """   
    
    raw_score = roll_result.count(2)*2
    return raw_score


def threes_value(roll_result, scores):
    """
    Calculate the score for the 'Threes' category in Yahtzee.
    
    Parameters:
    - roll_result (list): a list of integers representing the face values of the dice.
    - scores (dict): a dictionary representing the scores for each category.
    
    Returns:
    - (int): the score for the 'Threes' category.
    """

    raw_score = roll_result.count(3)*3
    return raw_score

    
def fours_value(roll_result, scores):
    """
    Calculate the score for the 'Fours' category in Yahtzee.
    
    Parameters:
    - roll_result (list): a list of integers representing the face values of the dice.
    - scores (dict): a dictionary representing the scores for each category.
    
    Returns:
    - (int): the score for the 'Fours' category.
    """

    raw_score = roll_result.count(4)*4
    return raw_score
    
    
def fives_value(roll_result, scores):    
    """
    Calculate the score for the 'Fives' category in Yahtzee.
    
    Parameters:
    - roll_result (list): a list of integers representing the face values of the dice.
    - scores (dict): a dictionary representing the scores for each category.
    
    Returns:
    - (int): the score for the 'Fives' category.
    """
    
    raw_score = roll_result.count(5)*5
    return raw_score
    

def sixes_value(roll_result, scores):    
    """
    Calculate the score for the 'Sixes' category in Yahtzee.
    
    Parameters:
    - roll_result (list): a list of integers representing the face values of the dice.
    - scores (dict): a dictionary representing the scores for each category.
    
    Returns:
    - (int): the score for the 'Sixes' category.
    """
    
    raw_score = roll_result.count(6)*6
    return raw_score




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
       
        
        
def score_category(category, roll_result, scores):
        
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
    




        
def score_game(scores):
    
    """
    Calculate the total score for a Yahtzee game.
    
    Parameters:
    - scores (dict): a dictionary representing the scores for each category.
    
    Returns:
    - (int): the total score for the game.
    """
    
    block_1_score = scores["ones"] + scores["twos"] + \
                    scores["threes"] + scores["fours"] + \
                    scores["fives"] + scores["sixes"]
    
    if block_1_score >= 63:
        block_1_score += 35
        
    block_2_score = scores["three-of-a-kind"] + scores["four-of-a-kind"] + \
                    scores["full-house"] + scores["small-straight"] + \
                    scores["large-straight"] + scores["yahtzee"] + \
                    scores["chance"]
    
    
    return block_1_score + block_2_score

        
def get_block_1_score(scores):
    
    """
    Calculate the score for the first block of categories in Yahtzee.
    
    Parameters:
    - scores (dict): a dictionary representing the scores for each category.
    
    Returns:
    - (int): the score for the first block of categories.
    """
    
    return scores["ones"] + scores["twos"] + \
           scores["threes"] + scores["fours"] + \
           scores["fives"] + scores["sixes"]
                    
           
def get_block_2_score(scores):
    
    """
    Calculate the score for the second block of categories in Yahtzee.
    
    Parameters:
    - scores (dict): a dictionary representing the scores for each category.
    
    Returns:
    - (int): the score for the second block of categories.
    """

    return scores["three-of-a-kind"] + scores["four-of-a-kind"] + \
           scores["full-house"] + scores["small-straight"] + \
           scores["large-straight"] + scores["yahtzee"] + \
           scores["chance"]
    
           

def has_bonus(scores):
    
    """
    Check if the score for the first block of categories in Yahtzee is high enough to receive a bonus.
    
    Parameters:
    - scores (dict): a dictionary representing the scores for each category.
    
    Returns:
    - (bool): 'True' if the score for the first block of categories is high enough to receive a bonus, 'False' otherwise.
    """
    
    block_1_score = scores["ones"] + scores["twos"] + \
                    scores["threes"] + scores["fours"] + \
                    scores["fives"] + scores["sixes"]
    
    if block_1_score >= 63:
        return True
    else: 
        return False
    





        
        
        
        