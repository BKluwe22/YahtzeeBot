import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc


dash.register_page(__name__, path="/strategy-overview")

layout = html.Div(
    children=[
        dcc.Markdown("""
## Introduction

I grew up playing Yahtzee on a near daily basis (more specifically, the German version Kniffel). Yet, I have somehow managed 
to consistently lose to people that have never played the game. My frustration 
finally boiled over near the end of last year when I lost six games in a row against an 
someone that I regarded as using inferior strategies (a.k.a. using "vibes").
As a result, I created a practice application for myself and anyone 
who 1. manages to find this, 2. wants to play Yahtzee on a computer (get the board game it's more fun). There are two
parts to this project. First, I tried to code up a general strategy for playing 
the game. The second was creating a usable (hopefully) game interface. 

Notably, Solitaire Yahtzee was already solved by Tom Verhoeff from the University of Eindhoven
over two decades ago. The technical definition of solving the game here is finding the move
in any given state of the game that maximizes the expected value and minimizes the variance.
He has a training application [here](http://www-set.win.tue.nl/~wstomv/misc/yahtzee/osyp.php).
If your goal is to become the best Yahtzee player on Earth over a sufficiently large number of 
games, please use his application, not mine. 

Others have created Yahtzee bots like Dion Hafner ([blog link](https://dionhaefner.github.io/2021/04/yahtzotron-learning-to-play-yahtzee-with-advantage-actor-critic/))
that have reached very strong performance. If you have somehow stumbled 
upon this app before reading his implementation, please look at his methods as they are very 
interesting. 

I did not look at other solutions until after finalizing my strategy. I
would have saved me from tearing out my hair a few times but I ended up finding
a pretty good approach that is at least somewhat different than other implementations. 

### Game Variant
I should note that I coded everything in line with the rules my family plays. It is very similar
to the classic rules where the only exception is the way that we handle the “Super Yahtzee” or “Bonus Kniffel”.
We only allow the “Bonus Kniffel” to be filled for the second block (three-of-a-kind, four-of-a-kind, full-house, 
small-straight, large-straight, and chance) only if the Kniffel has been previously achieved. There is no restriction 
here based on the state of Block 1. You do not have to fill the category corresponding to the dice that you achieved Kniffel with.


### Summary of Various Failed and Untested Approaches

#### Dynamic Programming, Q-learning

My initial approach was to try to use basic value/policy iteration / Q-learning. As you can probably guess, I quickly realized 
that the state space was far too large to keep in memory. There are 252 unique ordered combinations of five dice.
Given the fact that you aren't making any decisions on the first roll of the dice of every turn, 
you have a maximum of 3 decisions per turn. In terms of dice & rolls_left, there are 756 combinations which is trivial in terms of size. However, there are 8192 possible filled/unfilled states for the score sheet. 
Next, the combination of possible scores across categories greater than 8 billion. 

Looking back I should have spent more time here figuring out ways to compress the state space. 

#### Deep-Q Learning

Given the size of the state space, the next obvious choice was to use a neural network.
Several aspects made the DQN approach tricky. To start, I tried to make
an OpenAI Gym environment but ran into a lot of trouble. Specifically, I had issues 
with the dependency of the action space on the state. I do like the general style of 
the Gym Env and implemented the same reset and step methods in my class. 

A clear concern was ensuring that the agent did not take illegal actions. To combat this, I added an action mask to returned observation dictionary. I used PyTorch
to create a basic sequential neural network with three hidden layers with an input size 
of 255 and an output size of 223. I arrived at the output size as follows: there are 210 unique 
ordered combinations of holdout sets ((), (1,), (1,1), ... (6,6,6,6)) and 13 categories
(ones, twos, ..., chance). The features were the 5 dice, the number of rolls left, 
fill OrderedDict (1 == Filled, 0 == Unfilled for each category), score 
OrderedDict (integer values of each category), and an action mask array (1 == Legal, 0 == Illegal)
for each of the 223 possible actions. These inputs were all flattened.

In the forward method, I set the value of the illegal actions to the min value of a 
float64 in the output layer to ensure that they would never be chosen. I used ReLU activations
for all the hidden layers. 

I ran several experiments with a standard replay buffer. I used various epsilon decay 
schedules and hyperparameter combinations. Notably, since I only cared about the end score,
I used discount factors of 1 and 0.99 for the experiments.

Unfortunately, the best configuration of the DQN never achieved an average performance above ~210
over 500 games. I used the tensorboard plugin for PyTorch and tracked the score of all the 
categories for each game. The thing that stood out to me immediately was the sparsity of achieving
Yahtzee. If I remember correctly, it would only get Yahtzee in ~1/20,000 games. Additionally, it 
rarely achieved the bonus. I believe that Yahtzee can be categorized as a hard-exploration problem
meaning that it has to take sub-optimal steps to get to a better outcome. I think what was happening
was that it found moves that resulted in consistently good rewards early during training. With epsilon
decaying over time, the probability that it would continue to take those actions increased, leading
it to never explore actions that could result in Yahtzee. Consider a situation early in the game 
where it rolls four sixes and a four where Yahtzee and four-of-a-kind are open. Filling the 
four-of-a-kind results in a reward of 28. If you were to re-roll the four, you would still only have
a 1/6 chance of Yahtzee. On average, you would have to be in the position (or a similar one) an 
average of 6 times to find a possible Yahtzee. On top of that, you would have to pick Yahtzee over 
any other category which is unlikely early during training. This brings up another problem namely 
that if you don't choose Yahtzee early during the game when you have it, the probability that you
then get a super Yahtzee is very close to zero. As such, I think that there was never an awareness 
of the fact that super Yahtzee is even a possibility.  

I tried several modifications to the DQN as outlined in the Rainbow paper including Double DQN, 
Prioritized Experience Replay, and multi-step learning. Unfortunately, they were not enough to 
overcome this problem. Additionally, I tried several modifications to the reward function but 
again they failed. 

As a final note on the DQN approach, I eventually ran out of patience and moved on. One severe 
limitation of my experiment was the "relatively" small number of games I let the agent play. 
Ideally, I would have parallelized the training and had a slower epsilon decay. However, the 
hardware I have didn't allow for this to complete within a time frame that matched my level
of patience. Also, I didn't want to pay for any cloud instances.


#### Policy-Based Methods

I didn't use any policy-based methods. Policy-based methods like PPO are probably better for a 
problem like this. I honestly just got a bit frustrated with the sample inefficiencies of RL approaches.
Perhaps sometime in the future.

### Final Model

Based on my failure with the DQN, I concluded that I would need to have an agent
with at least some sort of model of the game. To my great dismay, I also recognized that I 
needed to lower the bar from only being happy with a model that was perfect to one that was
only pretty good. 

To begin, I reframed the problem from - what is the best action given the global game state? to 
what is the best action given the state of the turn if I want to maximize the score of 
each category?

If you think about playing Yahtzee, there are a lot of actions that you can take. However, 
there is usually only one or sometimes two rational moves if you want to 
maximize the expected value for a category at the end of a turn. 

I decided to build out a "round q-table". This is a nested dictionary where the top level has 19 keys which are tuples of
the category and a nullable variable for whether super Yahtzee was possible. For example,
this would be (category, None) in the Block 1 categories + Yahtzee and (category, True or False)
for the Block 2 categories (excluding Yahtzee).
The value of the top-level dictionary is another dictionary 
where the keys correspond to a tuple of dice and rolls left (i.e.: (1,2,2,3,4), 2). The values
correspond to the legal actions that can be taken in this state which are the legal holdout sets
corresponding to the dice and "END" meaning that you finish the turn. When there are 0 rolls left, 
the only legal action is "END".

This table was filled backward meaning that the values of END actions when rolls_left == 0 
were calculated first. Then I calculated the expected values of each legal action for all the 
states GIVEN that you take the best (highest expected value) move in the state resulting
from the current action. 

The tricky part here was accounting for the bonus. You cannot value the block 1 categories
simply as the way that they are scored on the score sheet. You must consider that 
you will get an additional 35 points if you score 63 or above in Block 1. Therefore, for the 
"round q-table", I valued a state with 3-of-a-kind dice higher than their raw value. Additionally, 
I valued states with 4-of-a-kind dice even higher as this provides an added cushion to your 
chances of getting the bonus at the end of the game.

```python

def n_value(roll_result: tuple, n: int) -> Union[int, float]:

    # n here can be 1,2,3,4,5, or 6 corresponding to the category  
    n_count = roll_result.count(n)
    raw_value = n_count*n
    
    if n_count == 3:
        return raw_value + (raw_value*35)/63
    elif n_count >= 4:
        return raw_value + ((raw_value*35)/63) + ((n*35)/21)
    else: 
        return raw_value
```

After having calculated the "round q-table", the next question would be: how do you use it for decision-making?

We first have to filter the table to find the possible moves given the state of the 
game. The top-level key is (category, super_yahtzee_possible ). We filter the dictionary based on the open categories
and whether Yahtzee has been previously achieved. Then we filter the next dictionary which has the key (dice, rolls_left).
After this, we have all of the legal moves that we could take in the current game state for all the open categories. 

This is where a previous observation comes in. There can only be one or two rational
moves if you want to maximize the expected value of a category at the end of the round.

This simply corresponds to extracting the action from each of the open categories that correspond to the 
highest expected value. If we do this for all the open categories, we now have a list of 
the best actions given a target category. 

Unfortunately, this is not where it ends. We still have to filter this list of actions down to the 
best (or at least hopefully a very good one). Your first thought might be to just take the 
action with the highest total expected value from the previous step. However, this is not a good 
strategy. Suppose you only have the block 1 categories left to fill. 
You roll four 1s and one 6 on your first roll.
Now you have two rolls left. Anyone can tell you that you should go for the ones. 
However, if this scenario were presented to the strategy above, it would hold out the 
six and re-roll. Why? The total expected value of the sixes is much higher.
Even the EV here for the sixes is about ~16 while for the ones it is 4.305. We have to somehow 
account for the relative value of the ones here. The reason why you go for the ones is 
that you probably think "I'm not going to get a better chance than this for the ones". 

Luckily, we can easily get the expected value for any category given we choose the best move 
for each category. The approach goes as follows. Suppose roll the dice for the initial roll. 
Here we have no control over the holdout set as it is always empty. We have a holdout -> outcome 
transition probability lookup table so we know the exact probability of arriving at any state 
after the first roll. In this next state, we simply look up the best action from the "round qtable"
and multiply it by the probability of getting that outcome on the first roll. We add up all of those
values and arrive at the expected value of the target category: 
    
```python
# round_ev_for_target_strategy keys are the 19 top-level keys mentioned above

empty_roll_pr_distribution = get_holdout_x_roll_probability_lookup()[()]    
for target in round_ev_for_target_strategy.keys():     
    target_ev = 0 
    for r1_outcome, r1_probability in empty_roll_pr_distribution.items():
        qvalues_for_outcome = qtable[(r1_outcome, 2)][target]
        highest_qvalue = max(qvalues_for_outcome.values())
        target_ev += ( highest_qvalue * r1_probability )
        
    round_ev_for_target_strategy[target] = target_ev 
```

Here are the bonus-adjusted expected values: 
```
('ones', None): 2.9373299244702578
('twos', None): 5.874659848940508
('threes', None): 8.811989773410732
('fours', None): 11.749319697880999
('fives', None): 4.686649622351215
('sixes', None): 17.623979546821467
('three-of-a-kind', False): 15.194661292951626
('three-of-a-kind', True): 17.900858489877045
('four-of-a-kind', False): 5.6112634276723545
('four-of-a-kind', True): 9.183306272474274
('full-house', False): 9.07207196300953
('full-house', True): 1.637540961743637
('small-straight', False): 18.463269387108188
('small-straight', True): 18.907594933123633
('large-straight', False): 10.44380066936457
('large-straight', True): 11.495289531787169
('yahtzee', None): 2.301432126284947
('chance', False): 23.33333333333333
('chance', True): 24.92945803194904s
```

Now that we have these values, we can adjust our decision-making process. After
we filter the "round q-table" and extract the best actions for all the categories,
we can subtract the expected values corresponding to each category to get an 
estimate of how "relatively good" the move is. 

Are we done? 

Unfortunately not. We have yet to account for another great annoyance that arises
from using this method. Namely, what happens if there are multiple categories
that have the same best move? 

If this is also the move with the highest relative value, this is not a problem. We
simply choose it. However, what if there is another action that has the highest 
relative value but there is another action for two other categories that are close 
behind? It might make sense to go for that action because it covers more categories. 

That being said, if the category with the highest relative value is far and away better, 
we might just want to ignore that option. 

Through trial & error and simulation, I found that a good way to handle this was to 
exponentiate the relative values ($$e^{p*x}$$) and sum them up for every action. 
I simulated 10,000 games varying p between 0.1 and 1.5 (step=0.1) and found that values
between 0.3-0.7 were the best so I just went with 0.5 as it is a nice number. 

The reason this works well is because this function "rewards" higher relative 
values in a non-linear fashion which increases the likelihood that really good
moves are not superseded by an action that is good for a bunch of categories. 
However, if there is an action with a relative value that is just a bit better
then the next best action which is good for two or more categories, we will 
choose that one. 

This model scores an average of 240.84767 and a median of 241 over 1,000,000 simulated games.
This is pretty good but it is still far from the solution (mean: 254) from Tom Verhoeff. 

After this, I made the user interface to play "against" this strategy. Notably,
I use "against" in quotes because the bot is not factoring the state of your score
sheet in any way shape or form. It is simply a solitaire Yahtzee strategy. However, 
I think it is more fun like this. 

### Additional Sort-Of Failure?
I have an unfortunate bend toward perfectionism. Even though the performance is
good, I thought it could still be improved.

Usually, when you have a good model, you can use your strategy to simulate a number of 
decisions ahead to see which is best. One example is Monte Carlo Tree Search
which is most commonly used with zero-sum two-player games like Chess or Go (see AlphaGo from DeepMind). 

Simulation with Yahtzee is quite tricky. Yahtzee is, in large part, a game of chance. This is
what I tell myself when I lose. However, it is also a game of skill. This is what I tell myself when
I win. There are a maximum of 39 decisions that you make per game. If you were to start simulating three
different actions and then play in accordance with your strategy in parallel with a maximum of five decisions 
left in an arbitrary legal state, you could compare the quality of the three actions
with high confidence after say 500 simulations per action. This is simply due to the fact that at this stage, 
the game tree is shallow. Basing a decision with 37 decisions left in the game, however, would require a very large 
number of simulations. If you are interested, you can simulate any number of legal actions for any 
given state for any number of times in parallel on the dashboard page. 

I wanted to try adding simulation anyway. My approach at first was to just simulate the top 3 best actions recommended
by the model in parallel $$100*(max\_num\_decisions\_left)$$. I used the Mann-Whitney U test to compare the two actions with 
the highest median scores (Yahtzee game score distributions are not normal - check the score distribution on 
the benchmark page). I chose the action that had the highest value for each decision. 

As you can imagine, it took a very long time to complete a game. Some decisions were overridden via the 
simulation step. I think a model with simulation is probably better but I have no way to do a proper benchmark without
letting my computer run for a few months :(
    
Honestly, I don't know if $$100*(max\_num\_decisions\_left)$$ simulated games are enough. It is likely that 
more is better in this case.    

 """, mathjax=True),
 
 html.Br(),
 html.Br(),
 html.Br(),

 html.H3("The End", style={ 'textAlign': 'center' }),
 
 html.Br(),
 html.Br(),
 html.Br()
 
 
    ], style = {
        'width': '75%',    
        'justifyContent': 'center',
        'margin-top': '5%', 
        'margin-left': 'auto',
        'margin-right': 'auto'
    }
)
        
        
        
        
        
        
        
        
        
        
        
        
