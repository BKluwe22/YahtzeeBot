from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd 
import plotly.express as px
import numpy as np 
import pickle
import itertools

CATEGORY_SCORE_MAPPING = {

    "ones": [i for i in range(6)],
    "twos": [i*2 for i in range(6)],
    "threes": [i*3 for i in range(6)],
    "fours": [i*4 for i in range(6)],
    "fives": [i*5 for i in range(6)],
    "sixes": [i*6 for i in range(6)],
    "three_of_a_kind": [0, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                        21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 100],
    "four_of_a_kind": [0, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                       21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 100],
    "full_house": [0, 25, 100],
    "small_straight": [0, 30, 100],
    "large_straight": [0, 40, 100],
    "yahtzee": [0, 50],
    "chance": [0, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
               21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 100]
}


CATEGORIES = ["ones", "twos", "threes", "fours", "fives", "sixes",
              "three-of-a-kind", "four-of-a-kind", "full-house",
              "small-straight", "large-straight", "yahtzee",
              "chance"]

BLOCK_1_CATEGORIES = ["ones", "twos", "threes", "fours", "fives", "sixes"]
BLOCK_2_CATEGORIES = ["three-of-a-kind", "four-of-a-kind", "full-house",
                      "small-straight", "large-straight", "yahtzee",
                      "chance"]


SUPER_YAHTZEE_CANDIDATES = [
    "three-of-a-kind", "four-of-a-kind", "full-house", "small-straight", 
    "large-straight", "chance"
]

CATEGORY_ROW_DATA = {
    
    "ones": {
         "l": html.Td([
                 html.Div([
                     html.P("Ones"), 
                     html.I(className="bi bi-dice-1"),
                     html.I(className="bi bi-dice-1"),
                     html.I(className="bi bi-dice-1"),
                     html.P("=3")
                 ], style={ 'display': 'inline-flex', 
                            'fontSize': 'large',
                            'columnGap': '0.5em' })                            
              ], style={ 'display': 'flex', 
                        'justifyContent': 'center', 
                        'marginLeft': 'auto', 
                        'marginRight': 'auto' }),  
                        
         "m": html.Td("COUNT AND ADD ONLY ONES",
                      style={ 'width': '25%', 'fontSize': 'small', 'textAlign': 'center' }),

    }, 
    "twos": {
        "l": html.Td([
                html.Div([
                    html.P("Twos"), 
                    html.I(className="bi bi-dice-2"),
                    html.I(className="bi bi-dice-2"),
                    html.I(className="bi bi-dice-2"),
                    html.P("=6")
                ], style={ 'display': 'inline-flex', 
                           'fontSize': 'large',
                           'columnGap': '0.5em' })                            
             ], style={ 'display': 'flex', 
                       'justifyContent': 'center', 
                       'marginLeft': 'auto', 
                       'marginRight': 'auto' }),  
                       
        "m": html.Td("COUNT AND ADD ONLY TWOS",
                     style={ 'width': '25%', 'fontSize': 'small', 'textAlign': 'center' }),
        
    },
    "threes": {
        "l": html.Td([
                html.Div([
                    html.P("Threes"), 
                    html.I(className="bi bi-dice-3"),
                    html.I(className="bi bi-dice-3"),
                    html.I(className="bi bi-dice-3"),
                    html.P("=9")
                ], style={ 'display': 'inline-flex', 
                           'fontSize': 'large',
                           'columnGap': '0.5em' })                            
             ], style={ 'display': 'flex', 
                       'justifyContent': 'center', 
                       'marginLeft': 'auto', 
                       'marginRight': 'auto' }),  
                       
        "m": html.Td("COUNT AND ADD ONLY THREES",
                     style={ 'width': '25%', 'fontSize': 'small', 'textAlign': 'center' }),
        
    },
    "fours": {
        "l": html.Td([
                html.Div([
                    html.P("Fours"), 
                    html.I(className="bi bi-dice-4"),
                    html.I(className="bi bi-dice-4"),
                    html.I(className="bi bi-dice-4"),
                    html.P("=12")
                ], style={ 'display': 'inline-flex', 
                           'fontSize': 'large',
                           'columnGap': '0.5em' })                            
             ], style={ 'display': 'flex', 
                       'justifyContent': 'center', 
                       'marginLeft': 'auto', 
                       'marginRight': 'auto' }),  
                       
        "m": html.Td("COUNT AND ADD ONLY FOURS",
                     style={ 'width': '25%', 'fontSize': 'small', 'textAlign': 'center' }),
        
    }, 
    "fives": {
        "l": html.Td([
                html.Div([
                    html.P("Fives"), 
                    html.I(className="bi bi-dice-5"),
                    html.I(className="bi bi-dice-5"),
                    html.I(className="bi bi-dice-5"),
                    html.P("=15")
                ], style={ 'display': 'inline-flex', 
                           'fontSize': 'large',
                           'columnGap': '0.5em' })                            
             ], style={ 'display': 'flex', 
                       'justifyContent': 'center', 
                       'marginLeft': 'auto', 
                       'marginRight': 'auto' }),  
                       
        "m": html.Td("COUNT AND ADD ONLY FIVES",
                     style={ 'width': '25%', 'fontSize': 'small', 'textAlign': 'center' }),
        
    },  
    "sixes": {
        "l": html.Td([
                html.Div([
                    html.P("Sixes"), 
                    html.I(className="bi bi-dice-6"),
                    html.I(className="bi bi-dice-6"),
                    html.I(className="bi bi-dice-6"),
                    html.P("=18")
                ], style={ 'display': 'inline-flex', 
                           'fontSize': 'large',
                           'columnGap': '0.5em' })                            
             ], style={ 'display': 'flex', 
                       'justifyContent': 'center', 
                       'marginLeft': 'auto', 
                       'marginRight': 'auto' }),  
                       
        "m": html.Td("COUNT AND ADD ONLY SIXES",
                     style={ 'width': '25%', 'fontSize': 'small', 'textAlign': 'center' }),
        
    },  
    
    "three-of-a-kind": {
        "l": html.Td("3 Of a kind", style={ 'textAlign': 'center' }),
        "m": html.Td("ADD TOTAL OF ALL DICE", style={ 'width': '25%', 'fontSize': 'small', 'textAlign': 'center' }),      
    },
        
    "four-of-a-kind": {
        "l": html.Td("4 Of a kind", style={ 'textAlign': 'center' }),
        "m": html.Td("ADD TOTAL OF ALL DICE", style={ 'width': '25%', 'fontSize': 'small', 'textAlign': 'center' }),      
    },
    
    "full-house": {
        "l": html.Td("Full House", style={ 'textAlign': 'center' }),
        "m": html.Td("SCORE 25", style={ 'width': '25%', 'fontSize': 'small', 'textAlign': 'center' }),        
    },
    
    "small-straight": {
        "l": html.Td("Sm. Straight", style={ 'textAlign': 'center' }),
        "m": html.Td("SCORE 30", style={ 'width': '25%', 'fontSize': 'small', 'textAlign': 'center' }),        
    },
    
    "large-straight": {
        "l": html.Td("Lg. Straight", style={ 'textAlign': 'center' }),
        "m": html.Td("SCORE 40", style={ 'width': '25%', 'fontSize': 'small', 'textAlign': 'center' }),        
    },
    
    "yahtzee": {
        "l": html.Td("YAHTZEE (5 of a kind)", style={ 'textAlign': 'center' }),
        "m": html.Td("SCORE 50", style={ 'width': '25%', 'fontSize': 'small', 'textAlign': 'center' }),        
    },
    "chance": {
        "l": html.Td("Chance", style={ 'textAlign': 'center' }),
        "m": html.Td("SCORE TOTAL OF ALL 5 DICE", style={ 'width': '25%', 'fontSize': 'small', 'textAlign': 'center' }),        
    },
    
}
                       


with open('round-qtable.pckl', 'rb') as f:
    round_qtable = pickle.load(f)
    
with open('round-evs.pckl', 'rb') as f:
    round_evs = pickle.load(f)



def format_scores(player_block_1_score, player_block_2_score, bot_block_1_score, bot_block_2_score):
    
    player_bonus = 35 if player_block_1_score >= 63 else 0
    bot_bonus = 35 if bot_block_1_score >= 63 else 0
    
    player_scores = html.Div([
        html.P(f"Block 1: {player_block_1_score}"),
        html.P(f"Block 2: {player_block_2_score}"),
        html.P(f"Total: {player_block_1_score+player_block_2_score+player_bonus}")
    ], style = { 'display': 'flex', 'columnGap': '15%', 'justifyContent': 'space-between',
                 'whiteSpace': 'nowrap' })

    bot_scores = html.Div([
        html.P(f"Block 1: {bot_block_1_score}"),
        html.P(f"Block 2: {bot_block_2_score}"),
        html.P(f"Total: {bot_block_1_score+bot_block_2_score+bot_bonus}")
    ], style = { 'display': 'flex', 'columnGap': '15%', 'justifyContent': 'space-between',
                 'whiteSpace': 'nowrap' })

    return player_scores, bot_scores


def get_player_scores_x_fills(game_state):
    
    player_scores = {k.replace('-state-player', ''): v['score'] for k, v in game_state.items()
                     if 'player' in k}

    player_fills = {k.replace('-state-player', ''): v['filled'] for k, v in game_state.items()
                    if 'player' in k}

    return player_scores, player_fills
                
                
def get_bot_scores_x_fills(game_state):
    
    bot_scores = {k.replace('-state-bot', ''): v['score'] for k, v in game_state.items()
                  if 'bot' in k}

    bot_fills = {k.replace('-state-bot', ''): v['filled'] for k, v in game_state.items()
                 if 'bot' in k}
                
    return bot_scores, bot_fills
                
                
def generate_score_sheet_blocks(player: bool, category_scores: dict, current_fills: dict, current_scores: dict):       
    
    block1_children = []
    block2_children = []
    
    for category, category_score in category_scores.items():
    
        if category in BLOCK_1_CATEGORIES:
            block1_children.append(
                score_sheet_row(
                    category=category,
                    player=player,
                    score=current_scores[category],
                    filled=True if current_fills[category] else False,
                    score_text=current_scores[category] if current_fills[category] else f"+{category_score}",
                    disabled=True if current_fills[category] else False)
            )
        else:
            block2_children.append(
                score_sheet_row(
                    category=category,
                    player=player,
                    score=current_scores[category],
                    filled=True if current_fills[category] else False,
                    score_text=current_scores[category] if current_fills[category] else f"+{category_score}",
                    disabled=True if current_fills[category] else False)
            )
            
    return block1_children, block2_children
                    


def generate_dice_output(prior_holdouts, new_dice):
    
    
    prior_holdout_children = []
    new_dice_children = []
    
    for idx, die in enumerate(prior_holdouts):
        prior_holdout_children.append(
            dbc.Button(
                id={
                    "type": 'dice-btn', "index": idx
                },
                children=html.H1( html.I(className=f"bi bi-dice-{die}") ),
                style={'fontSize': 'large'},
                size='lg',
                color='dark',
                outline=True,
                value=die,
            )
        )  
    
    for new_die in new_dice: 
        
        new_dice_children.append(
            dbc.Button(
                id={
                    "type": 'dice-btn', "index": len(prior_holdout_children + new_dice_children)
                },
                children=html.H1(
                    html.I(className=f"bi bi-dice-{new_die}")),
                style={'fontSize': 'large'},
                size='lg',
                color='dark',
                outline=True,
                value=new_die,
            )
        )  
    
    dice_children = html.Div([
        html.Div(prior_holdout_children, style={ 'whiteSpace': 'nowrap' }),
        html.Div(new_dice_children, style={ 'whiteSpace': 'nowrap' })
    ], style={
        'display': 'flex',
        'justifyContent': 'center', 
        'columnGap': '5%',
        'width': '100%',
    })
        
    return dice_children


def generate_game_summary(action_data, player_bonus, bot_bonus, player_final_score, bot_final_score):
    
    text_style = { 'whiteSpace': 'no-wrap', 'textAlign': 'center' }
        
    return html.Div([
        
        html.Div([
            
            html.H5(["Block 1", dbc.Badge(action_data['game-ctrl']['player-block-1-score'], color="dark")], style=text_style),
            html.H5(["Bonus", dbc.Badge(player_bonus, color="dark")], style=text_style),
            html.H5(["Block 2", dbc.Badge(action_data['game-ctrl']['player-block-2-score'], color="dark")], style=text_style),
            html.H5(["Total", dbc.Badge(player_final_score, color="dark")], style=text_style),

        ]), 
        
        html.Div([
             
            html.H5(["Block 1", dbc.Badge(action_data['game-ctrl']['bot-block-1-score'], color="dark")], style=text_style),
            html.H5(["Bonus", dbc.Badge(bot_bonus, color="dark")], style=text_style),
            html.H5(["Block 2", dbc.Badge(action_data['game-ctrl']['bot-block-2-score'], color="dark")], style=text_style),
            html.H5(["Total", dbc.Badge(bot_final_score, color="dark")], style=text_style),

        ])
        
    ], style = { 
        'display': 'flex', 
        'justifyContent': 'space-between', 
        'width': '75%',
        'columnGap': '25%'
    })

                
                
def relative_ev_chart(relative_ev_data: dict, height: int = 350):
    
    df = pd.DataFrame.from_dict(relative_ev_data, orient="index", columns=["value_vs_ev"]).reset_index()
    
    df[['target', 'action']] = df['index'].tolist()

    df.drop(["index"], axis=1, inplace=True)
    
    df["action"] = df["action"].astype(str) 

    # df['raw_value'] = df['target'].apply(lambda x: scoring.score_category(x, dice, scores))    
    fig = px.bar(df, x="target", y="value_vs_ev", color="action", template="simple_white",
                 labels={
                     "value_vs_ev": "Relative Value",
                     "target": "Category",
                     "action": "Action (Holdout or Category)"
                 },
                 title="Action Value vs. Bonus Adjusted Expected Value for Category | Policy",
                 height=height
    )
    
    return fig


def decision_chart(action_ranking_data: dict, height: int = 350):    

    df = pd.DataFrame.from_dict(action_ranking_data, orient="index", columns=["exp_relative_value"]).reset_index()
    
    df.columns = ['action', 'exp_relative_value']
    
    df["action"] = df["action"].astype(str) 

    # df['raw_value'] = df['target'].apply(lambda x: scoring.score_category(x, dice, scores))    
    fig = px.bar(df, x="action", y="exp_relative_value", template="simple_white",
                  labels={
                      "exp_relative_value": "Exponentiated Relative Value",
                      "action": "Action",
                  },
                  title="Exponentiated Relative Value | Policy",
                  height=height
    )
    
    return fig



def bot_decision_modal(decision_data: dict):
    
    dice = decision_data['state']['dice']
    rolls_left = decision_data['state']['rolls_left']
    
    dice_div_children = []
    for d in dice: 
        dice_div_children.append(
            html.H1(html.I(className=f"bi bi-dice-{d}"))        
        )
    
    dice_div = html.Div(children=dice_div_children,
                        style={ 
                            'display': 'flex',
                            'flexDirection': 'row' 
                        }
    )
    
    
    modal = html.Div([
            dbc.Button("Show Decision Logic", id="open-modal-{}".format(decision_data['state']['rolls_left'])),
            dbc.Modal(
                [
                    dbc.ModalBody(children=html.Div([
                        html.P("Rolls Left: {}".format(rolls_left)),
                        dice_div,
                        dcc.Graph(figure=relative_ev_chart(decision_data["relative_action_values"])),
                        html.Br(), 
                        dcc.Graph(figure=decision_chart(decision_data['action_ranking']))
                    ])),
                ],
                id="modal-{}".format(decision_data['state']['rolls_left']),
                size="xl",
                is_open=False,
            ),
    ], style = { 'alignSelf': 'center' })
    
    return modal


                
def bot_decision_summary(decision_data: dict):
    
    dice = decision_data['state']['dice']
    rolls_left = decision_data['state']['rolls_left']
    
    dice_div_children = []
    for d in dice: 
        dice_div_children.append(
            html.H1(html.I(className=f"bi bi-dice-{d}"))        
        )
    
    dice_div = html.Div(children=dice_div_children,
                        style={ 
                            'display': 'flex',
                            'flexDirection': 'row' 
                        }
    )
    
    return dbc.Card(
                dbc.CardBody([
                    
                        html.Div([
                            html.P(f"Rolls Left: {rolls_left}"),    
                            dice_div, 
                            html.P("Decision: {}".format(
                                decision_data['action'].upper() if isinstance(decision_data['action'], str) else "Holdout " + str(decision_data['action'])
                            ))                          
                        ], style = { 'display': 'flex', 'flexDirection': 'column' }), 
                        
                        bot_decision_modal(decision_data)
                
                ], style = {
                    'display': 'flex',
                    'flexDirection': 'row',
                    'justifyContent': 'space-around'                                    
                }),
            )
                    
                    
def format_game_data(turn: str,
                     rolls_left: int,
                     player_block_1_score: int, 
                     player_block_2_score: int,
                     bot_block_1_score: int,
                     bot_block_2_score: int, 
                     game_over: bool):
    
    return {
        
        'turn': turn,
        'rolls-left': rolls_left,
        
        'player-block-1-score': player_block_1_score,
        'player-block-2-score': player_block_2_score,

        'bot-block-1-score': bot_block_1_score,
        'bot-block-2-score': bot_block_2_score,
        
        'game-over': game_over
        
    }
    
    
                    


def block1_header():
    return html.Thead(
        html.Tr([
            html.Th("MINIMUM REQUIRED FOR BONUS", style={
                    'fontSize': 'small', 'textAlign': 'center'}),
            html.Th("HOW TO SCORE", style={
                    'fontSize': 'small', 'textAlign': 'center'}),
            html.Th("SCORE", style={
                    'fontSize': 'small', 'textAlign': 'center'})
        ])
    )


def block2_header():
    return html.Thead(
        html.Tr([
            html.Th("", style={'textAlign': 'center'}),
            html.Th("", style={'textAlign': 'center'}),
            html.Th("", style={'textAlign': 'center'})
        ])
    )


def score_sheet_row(category: str, player: bool, score: int, filled: bool, score_text: str, disabled: bool):

    return html.Tr([

        CATEGORY_ROW_DATA[category]["l"],
        CATEGORY_ROW_DATA[category]["m"],
        html.Td([
            dcc.Store(
                id=f"{category}-state-player" if player else f"{category}-state-bot",
                data={'score': score, 'filled': filled}),
            html.Div([
                dbc.Button(
                    score_text,
                    id={'type': 'player-item' if player else 'bot-item',
                        'index': category},
                    disabled=disabled,
                    size='sm',
                    color='light' if filled else 'primary'
                )
            ], style={'display': 'flex', 'justifyContent': 'center'})

        ], style={'width': '20%'})
    ])



def category_row_data(): 
    
    return {
        
        "ones": {
             "l": html.Td([
                     html.Div([
                         html.P("Ones"), 
                         html.I(className="bi bi-dice-1"),
                         html.I(className="bi bi-dice-1"),
                         html.I(className="bi bi-dice-1"),
                         html.P("=3")
                     ], style={ 'display': 'inline-flex', 
                                'fontSize': 'large',
                                'columnGap': '0.5em' })                            
                  ], style={ 'display': 'flex', 
                            'justifyContent': 'center', 
                            'marginLeft': 'auto', 
                            'marginRight': 'auto' }),  
                            
             "m": html.Td("COUNT AND ADD ONLY ONES",
                          style={ 'width': '25%', 'fontSize': 'small', 'textAlign': 'center' }),
    
        }, 
        "twos": {
            "l": html.Td([
                    html.Div([
                        html.P("Twos"), 
                        html.I(className="bi bi-dice-2"),
                        html.I(className="bi bi-dice-2"),
                        html.I(className="bi bi-dice-2"),
                        html.P("=6")
                    ], style={ 'display': 'inline-flex', 
                               'fontSize': 'large',
                               'columnGap': '0.5em' })                            
                 ], style={ 'display': 'flex', 
                           'justifyContent': 'center', 
                           'marginLeft': 'auto', 
                           'marginRight': 'auto' }),  
                           
            "m": html.Td("COUNT AND ADD ONLY TWOS",
                         style={ 'width': '25%', 'fontSize': 'small', 'textAlign': 'center' }),
            
        },
        "threes": {
            "l": html.Td([
                    html.Div([
                        html.P("Threes"), 
                        html.I(className="bi bi-dice-3"),
                        html.I(className="bi bi-dice-3"),
                        html.I(className="bi bi-dice-3"),
                        html.P("=9")
                    ], style={ 'display': 'inline-flex', 
                               'fontSize': 'large',
                               'columnGap': '0.5em' })                            
                 ], style={ 'display': 'flex', 
                           'justifyContent': 'center', 
                           'marginLeft': 'auto', 
                           'marginRight': 'auto' }),  
                           
            "m": html.Td("COUNT AND ADD ONLY THREES",
                         style={ 'width': '25%', 'fontSize': 'small', 'textAlign': 'center' }),
            
        },
        "fours": {
            "l": html.Td([
                    html.Div([
                        html.P("Fours"), 
                        html.I(className="bi bi-dice-4"),
                        html.I(className="bi bi-dice-4"),
                        html.I(className="bi bi-dice-4"),
                        html.P("=12")
                    ], style={ 'display': 'inline-flex', 
                               'fontSize': 'large',
                               'columnGap': '0.5em' })                            
                 ], style={ 'display': 'flex', 
                           'justifyContent': 'center', 
                           'marginLeft': 'auto', 
                           'marginRight': 'auto' }),  
                           
            "m": html.Td("COUNT AND ADD ONLY FOURS",
                         style={ 'width': '25%', 'fontSize': 'small', 'textAlign': 'center' }),
            
        }, 
        "fives": {
            "l": html.Td([
                    html.Div([
                        html.P("Fives"), 
                        html.I(className="bi bi-dice-5"),
                        html.I(className="bi bi-dice-5"),
                        html.I(className="bi bi-dice-5"),
                        html.P("=15")
                    ], style={ 'display': 'inline-flex', 
                               'fontSize': 'large',
                               'columnGap': '0.5em' })                            
                 ], style={ 'display': 'flex', 
                           'justifyContent': 'center', 
                           'marginLeft': 'auto', 
                           'marginRight': 'auto' }),  
                           
            "m": html.Td("COUNT AND ADD ONLY FIVES",
                         style={ 'width': '25%', 'fontSize': 'small', 'textAlign': 'center' }),
            
        },  
        "sixes": {
            "l": html.Td([
                    html.Div([
                        html.P("Sixes"), 
                        html.I(className="bi bi-dice-6"),
                        html.I(className="bi bi-dice-6"),
                        html.I(className="bi bi-dice-6"),
                        html.P("=18")
                    ], style={ 'display': 'inline-flex', 
                               'fontSize': 'large',
                               'columnGap': '0.5em' })                            
                 ], style={ 'display': 'flex', 
                           'justifyContent': 'center', 
                           'marginLeft': 'auto', 
                           'marginRight': 'auto' }),  
                           
            "m": html.Td("COUNT AND ADD ONLY SIXES",
                         style={ 'width': '25%', 'fontSize': 'small', 'textAlign': 'center' }),
            
        },  
        
        "three-of-a-kind": {
            "l": html.Td("3 Of a kind", style={ 'textAlign': 'center' }),
            "m": html.Td("ADD TOTAL OF ALL DICE", style={ 'width': '25%', 'fontSize': 'small', 'textAlign': 'center' }),      
        },
            
        "four-of-a-kind": {
            "l": html.Td("4 Of a kind", style={ 'textAlign': 'center' }),
            "m": html.Td("ADD TOTAL OF ALL DICE", style={ 'width': '25%', 'fontSize': 'small', 'textAlign': 'center' }),      
        },
        
        "full-house": {
            "l": html.Td("Full House", style={ 'textAlign': 'center' }),
            "m": html.Td("SCORE 25", style={ 'width': '25%', 'fontSize': 'small', 'textAlign': 'center' }),        
        },
        
        "small-straight": {
            "l": html.Td("Sm. Straight", style={ 'textAlign': 'center' }),
            "m": html.Td("SCORE 30", style={ 'width': '25%', 'fontSize': 'small', 'textAlign': 'center' }),        
        },
        
        "large-straight": {
            "l": html.Td("Lg. Straight", style={ 'textAlign': 'center' }),
            "m": html.Td("SCORE 40", style={ 'width': '25%', 'fontSize': 'small', 'textAlign': 'center' }),        
        },
        
        "yahtzee": {
            "l": html.Td("YAHTZEE (5 of a kind)", style={ 'textAlign': 'center' }),
            "m": html.Td("SCORE 50", style={ 'width': '25%', 'fontSize': 'small', 'textAlign': 'center' }),        
        },
        "chance": {
            "l": html.Td("Chance", style={ 'textAlign': 'center' }),
            "m": html.Td("SCORE TOTAL OF ALL 5 DICE", style={ 'width': '25%', 'fontSize': 'small', 'textAlign': 'center' }),        
        },
        
    }
                           
                           


def select_action(dice, rolls_left, scores, fills, n_best=1):
        
    open_categories = [ cat.replace('_', '-') for cat, fill_bool in fills.items() if fill_bool == False ]
                            
    super_yahtzee_possible = ( scores["yahtzee"] == 50 )
    
    lookup_keys = [ (cat, super_yahtzee_possible) if cat in SUPER_YAHTZEE_CANDIDATES 
                    else (cat, None) for cat in open_categories ]
        
    r_qtable = { k: v for k, v in round_qtable[(dice, rolls_left)].items()
                                  if k in lookup_keys }
            
    best_actions = {}
    exp_best_actions = {}
    for k, v in r_qtable.items(): 

        highest_value_relative_value_action_key = (max(v, key=v.get))
        
        highest_relative_value = v[highest_value_relative_value_action_key] - round_evs[k]
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

    return best_actions, exp_best_actions




def action_values_relative_to_ev(dice, rolls_left, scores, fills, height):
    
    data, _ = select_action(dice, rolls_left, scores, fills)

    df = pd.DataFrame.from_dict(data, orient="index", columns=["value_vs_ev"]).reset_index()

    df[['target', 'action']] = df['index'].tolist()

    df.drop(["index"], axis=1, inplace=True)
    
    df["action"] = df["action"].astype(str) 

    # df['raw_value'] = df['target'].apply(lambda x: scoring.score_category(x, dice, scores))    
    fig = px.bar(df, x="target", y="value_vs_ev", color="action", template="simple_white",
                 labels={
                     "value_vs_ev": "Relative Value",
                     "target": "Category",
                     "action": "Action (Holdout or Category)"
                 },
                 title="Action Value vs. Bonus Adjusted Expected Value for Category | Policy",
                 height=height
    )
    
    
    return fig, df
    

def action_value_probabilities(dice, rolls_left, scores, fills, height):
    
    _, data = select_action(dice, rolls_left, scores, fills)

    df = pd.DataFrame.from_dict(data, orient="index", columns=["exp_relative_value"]).reset_index()

    df.columns = ['action', 'exp_relative_value']
    
    df["action"] = df["action"].astype(str) 

    fig = px.bar(df, x="action", y="exp_relative_value", template="simple_white",
                  labels={
                      "exp_relative_value": "Exponentiated Relative Value",
                      "action": "Action",
                  },
                  title="Exponentiated Relative Value | Policy",
                  height=height
    )
    
    return fig, df



def simulation_candidates(dice, rolls_left, scores, fills):
        
    open_categories = [ cat.replace('_', '-') for cat, fill_bool in fills.items() if fill_bool == False ]
                            
    super_yahtzee_possible = ( scores["yahtzee"] == 50 )
    
    lookup_keys = [ (cat, super_yahtzee_possible) if cat in SUPER_YAHTZEE_CANDIDATES 
                    else (cat, None) for cat in open_categories ]
        

    available_actions = [ [ a if isinstance(a, tuple) else k[0] for a in v.keys() ] for k, v in round_qtable[(dice, rolls_left)].items()
                                 if k in lookup_keys ]

    available_actions = list(set(list(itertools.chain(*available_actions))))
    
    category_actions = [ a for a in available_actions if isinstance(a, str) ]
    holdout_actions = [ a for a in available_actions if isinstance(a, tuple) ]


    category_switches = html.Div(
        [
            dbc.Checklist(
                options=[
                    
                    { "label": x, "value": x } for x in category_actions
                ],
                id="category-simulation-switches",
                value=[],
                switch=True
            ),
        ]
    )
    
    holdout_switches = html.Div(
        [
            dbc.Checklist(
                options=sorted([                    
                    { "label": str(x), "value": x } for x in holdout_actions
                ], key=lambda item: item["value"]),
                id="holdout-simulation-switches",
                value=[],
                switch=True,
                style={
                    'display': 'grid',
                    'gridTemplateColumns': 'repeat(2, 3fr)',
                    'gridTemplateRows': 'repeat(13, 1fr)',
                    'columnGap': '50px',
                }
            ),
        ]
    )
    
    
    return html.Div([
        
         html.Div([
            html.H3("Simulate Decisions", { 'textAlign': 'center' }),
         ], style={'display': 'flex', 'justifyContent': 'center'}),
            
         html.Br(),
         html.Br(),

         html.Div([
             category_switches,
             html.Br(),
             holdout_switches
         ], style={ 'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-around' }),
         
         html.Br(),
         html.Br(),
         
         
    ], style={'display': 'flex', 'flexDirection': 'column', 'width': '100%' })


    

    
    
    
