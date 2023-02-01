import numpy as np 

def roll_dice(holdout: tuple = ()) -> tuple:
    """
    Roll the dice in the Yahtzee game.

    Parameters:
    - holdout (tuple): a tuple of integers representing the dice that should not be re-rolled.

    Returns:
    - (tuple): a tuple of integers representing the result of the dice roll.
    """
    sorted_input_tuple = tuple(sorted(holdout))

    rolled_dice = ()
    for _ in range(5-len(sorted_input_tuple)):
        rolled_dice += (np.random.choice(a=[1, 2, 3, 4, 5, 6]), )

    return sorted_input_tuple, tuple(sorted(rolled_dice))