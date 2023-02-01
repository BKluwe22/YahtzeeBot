from dash import html, dcc, Input, Output, State, callback, get_asset_url, ctx, MATCH, ALL
import dash
import dash_bootstrap_components as dbc
import true_scoring as scoring
from bot import YahtzeeBot
import fn_components
import utils

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

BLOCK_1_CATGEORY_NUM_VALUE_MAP = {
    "ones": 1,
    "twos": 2,
    "threes": 3,
    "fours": 4,
    "fives": 5,
    "sixes": 6,
}

BLOCK_1_CATEGORY_VALUE_DICE_SVG_MAP = {
    1: "one.svg",
    2: 'two.svg',
    3: 'three.svg',
    4: 'four.svg',
    5: 'five.svg',
    6: 'six.svg'
}


ACTIVE_BTN_STYLE = { 'width': '50%', 'marginLeft': 'auto', 
                     'marginRight': 'auto', 'display': 'block',
                     'alignSelf': 'center' }
HIDDEN_BTN_STYLE = { 'width': '50%', 'marginLeft': 'auto', 
                     'marginRight': 'auto', 'display': 'none',
                     'alignSelf': 'center' }



dash.register_page(__name__, path="/")



init_player_table = dbc.Table(children=[

    fn_components.block1_header(),
    html.Tbody(id='player-table-block1', children=[
        fn_components.score_sheet_row(category=cat, player=True, score=0,
                                      filled=False, score_text="0", disabled=True)
        for cat in BLOCK_1_CATEGORIES
    ]),
    html.Tbody([html.Tr([html.Td(""), html.Td(""), html.Td("")])]),
    html.Tbody(id='player-table-block2', children=[
        fn_components.score_sheet_row(category=cat, player=True, score=0,
                                      filled=False, score_text="0", disabled=True)
        for cat in BLOCK_2_CATEGORIES
    ]),

], bordered=True, style={'width': '100%'})


init_bot_table = dbc.Table(children=[

    fn_components.block1_header(),
    html.Tbody(id='bot-table-block1', children=[
        fn_components.score_sheet_row(category=cat, player=False, score=0,
                                      filled=False, score_text="0", disabled=True)
        for cat in BLOCK_1_CATEGORIES
    ]),
    html.Tbody([html.Tr([html.Td(""), html.Td(""), html.Td("")])]),
    html.Tbody(id='bot-table-block2', children=[
        fn_components.score_sheet_row(category=cat, player=False, score=0,
                                      filled=False, score_text="0", disabled=True)
        for cat in BLOCK_2_CATEGORIES
    ]),

], bordered=True, style={'width': '100%'})


layout = dbc.Container([


    html.Div([

        html.Div(
            id='player-table-container',
            children=[                
                
                html.Div([
                  html.P("Player 1", style={
                         'fontWeight': 'bold', 'textAlign': 'center'}),
                  html.Div(id='player-scoreboard'),
                ], style = { 'display': 'flex', 'justifyContent': 'space-evenly', 'width': '100%' }),
                            
                init_player_table
        ], style = { 'width': '30%' }),

        html.Div(id='player-sheet'),

        html.Div([

            html.Div(id='game-result'),
            
            html.Div(id='main-output', children=[],
                     style={
                        'display': 'flex',
                        'justifyContent': 'center',
                        'minHeight': '1%',
                        'minWidth': '50%'
                    }
            ),

            html.Br(),
            html.Br(),

            html.Br(),
            html.Br(),
            html.Br(),

            dcc.Store(id='game-ctrl',
                      data={           
                          
                          'turn': 'player',
                          'rolls-left': 3,                          
                          'player-block-1-score': 0,
                          'player-block-2-score': 0,
                          'bot-block-1-score': 0,
                          'bot-block-2-score': 0,
                          'game-over': False
                          
                      }
            ),

            dcc.Store(id='decision-ctrl',
                      data={
                          'decision': tuple(),
                          'dice': None
                      }
            ),

            dbc.Button('Start Turn', id='game-ctrl-btn', style=ACTIVE_BTN_STYLE),            
            dbc.Button(id='decision-ctrl-btn', style=HIDDEN_BTN_STYLE),
            
            html.Br(),
            html.Br(),
            html.Br(),
            
            dbc.Button(html.I(className="bi bi-question-circle"), 
                       id='open-instructions', 
                       color='dark',
                       outline=True,
                       size="md",
                       style={ 
                           'position': 'fixed', 
                           'bottom': '5%', 
                           'alignSelf': 'center'
                       }),
            
            
            dbc.Offcanvas(
                dcc.Markdown(
                    """
                    # Instructions\
                        
                    ### Bonus: 
                    You will get the Bonus worth 35 points if you score 63 or above in Block 1 (Ones, Twos, Threes, 
                    Fours, Fives, Sixes). 
                    
                    ### Rules:
                    
                    It is assumed that you have some baseline familiarity with Yahtzee/Knifle. 
                    The only distinguishing factor of this variant of the game is related to the Super Yahtzee or
                    Bonus Kniffle. You must have a 50 in the Yahtzee category before you can get the Super Yahtzee 
                    which is worth 100 points. Additionally, you can only use it for an open category in Block 2. 
                    There are no restrictions involving Block 1. For some variants, you must score the five-of-a-kind
                    in Block 1 first. This is not the case here. All other rules are inline with tradition. 
                    
                    ### User Interface:
                        
                    The game transitions (submitting decisions, starting rounds, showing the bot's turn)
                    are controlled by the central button. When you start your turn, there will be 5 random dice displayed
                    in the center of the screen. This marks you first roll. You can decide to either choose a category on
                    the score sheet to the left OR holdout a set of dice and re-roll. 
                    
                    Each item value on the score sheet will be computed for you based on the dice on the screen. You can 
                    select the category you wish to score by clicking on the red button associated with the category. Before 
                    you can select a category, you must ensure that none of the dice are green. If you have green dice, you
                    must deselect them first. The button will turn GREEN after you have selected it. If it is not green, 
                    it has not been properly selected. If you wish to choose another category you must first deselect the 
                    one that is currently green.
                    
                    Each of the dice can be selected to go into the holdout set. Please note that these are the dice that are
                    NOT being re-rolled. Like the categories, the buttons will turn green once they are properly selected. 
                    Unlike the categories, you can choose multiple dice. To remove a dice from the holdout set, click the 
                    dice again so that they are black. Once you submit the dice to be re-rolled, the dice that you chose
                    to be held out will be slightly set to the left of the new dice. This is to improve readability. 
                    In order to hold these dice out again, you must select them again so that they are green. 

                    Disclaimer: I sometimes make analytical dashboards with Plotly Dash. However, I know next to nothing
                    about frontend design or best practices. 
                    
                    ### Unfortunate Issues: 
                    If you refresh the page by accident, the game state will reset.                     
                    """
                ),
                id="instructions",
                placement="end",
                is_open=False,
                style={'width': '45%'}
            ),
                

        ], style={
            'display': 'flex',
            'flexDirection': 'column',
            'alignSelf': 'center',
            'width': '35%'
        }),

        html.Div(id='bot-sheet'),

        html.Div(
            id='bot-table-container',
            children=[
                html.Div([
                  html.P("Bot", style={
                         'fontWeight': 'bold', 'textAlign': 'center'}),
                  html.Div(id='bot-scoreboard'),
                ], style = { 'display': 'flex', 'justifyContent': 'space-evenly' }),
                            
                init_bot_table
            ], style = { 'width': '30%' }),

    ], style={
        'display': 'flex',
        'justifyContent': 'space-evenly',
    })


], fluid=True, style={
    'marginTop': '1%',
})

game_state_ids = []
for id_ in layout:
    if 'state' in id_:
        game_state_ids.append(id_)


def step_output(main_output: html.Div, 
                player_scoreboard: html.Div, 
                bot_scoreboard: html.Div, 
                game_ctrl_btn_c: html.P, 
                decision_ctrl_btn_c: html.P, 
                game_ctrl_btn_style: dict,
                decision_ctrl_btn_style: dict,                
                player_table_block1_c: html.Div, 
                player_table_block2_c: html.Div, 
                bot_table_block1_c: html.Div,
                bot_table_block2_c: html.Div, 
                game_ctrl_data: dict): 
    
    return [main_output, player_scoreboard, bot_scoreboard, game_ctrl_btn_c, decision_ctrl_btn_c, 
            game_ctrl_btn_style, decision_ctrl_btn_style, player_table_block1_c, 
            player_table_block2_c, bot_table_block1_c, bot_table_block2_c, game_ctrl_data]


@callback(
    [
        Output('main-output', 'children'),
        Output('player-scoreboard', 'children'),
        Output('bot-scoreboard', 'children'),

        Output('game-ctrl-btn', 'children'),
        Output('decision-ctrl-btn', 'children'),
        Output('game-ctrl-btn', 'style'),
        Output('decision-ctrl-btn', 'style'),

        Output('player-table-block1', 'children'),
        Output('player-table-block2', 'children'),
        Output('bot-table-block1', 'children'),
        Output('bot-table-block2', 'children'),

        Output('game-ctrl', 'data')

    ],

    inputs={

        "action_execution": {
            'game-ctrl-btn': Input('game-ctrl-btn', 'n_clicks'),
            'decision-ctrl-btn': Input('decision-ctrl-btn', 'n_clicks')
        },

        "action_data": {
            'game-ctrl': State('game-ctrl', 'data'),
            'decision-ctrl': State('decision-ctrl', 'data')
        },

        'score_sheet_blocks': {

            'player-table-block1': State('player-table-block1', 'children'),
            'player-table-block2': State('player-table-block2', 'children'),

            'bot-table-block1': State('bot-table-block1', 'children'),
            'bot-table-block2': State('bot-table-block2', 'children')
        },

        "game_state": {
            k: State(k, 'data') for k in game_state_ids
        }
    },
)


def step(action_execution,
         action_data,
         score_sheet_blocks,
         game_state):
    
    action_exec_ctx = ctx.args_grouping.action_execution
    
    if action_data['game-ctrl']['game-over']:
        
        player_bonus = 35 if action_data['game-ctrl']['player-block-1-score'] >= 63 else 0
        bot_bonus = 35 if action_data['game-ctrl']['bot-block-1-score'] >= 63 else 0

        player_final_score = action_data['game-ctrl']['player-block-1-score'] + action_data['game-ctrl']['player-block-2-score'] + player_bonus
        bot_final_score = action_data['game-ctrl']['bot-block-1-score'] + action_data['game-ctrl']['bot-block-2-score'] + bot_bonus
        
        if player_final_score > bot_final_score:
            heading = "You Won!!!"
            img = html.Img(src=get_asset_url('trophy.svg'))
        elif player_final_score < bot_final_score: 
            heading = "The Bot Won"
            img = html.Img(src=get_asset_url('robot.svg'))
        else: 
            heading = "You Tied!?!"            
        
        game_summary_div = fn_components.generate_game_summary(action_data, 
                                                               player_bonus,
                                                               bot_bonus,
                                                               player_final_score, 
                                                               bot_final_score)
        
        main_output = html.Div([
            html.H1(heading, style = { 'textAlign': 'center', 'fontWeight': 'bold' } ),
            html.Br(), 
            img, 
            html.Br(), 
            game_summary_div,
            html.Br(), 
            html.Br(), 
            html.P("Refresh the page to play again!")
        ], style = {
            'display': 'flex',
            'justifyContent': 'center',
            'alignItems': 'center', 
            'flexDirection': 'column'
        })
            
        player_scoreboard, bot_scoreboard = fn_components.format_scores(player_block_1_score=action_data['game-ctrl']['player-block-1-score'], 
                                                                      player_block_2_score=action_data['game-ctrl']['player-block-2-score'],
                                                                      bot_block_1_score=action_data['game-ctrl']['bot-block-1-score'], 
                                                                      bot_block_2_score=action_data['game-ctrl']['bot-block-2-score'])
                    
                    
        return step_output(main_output=main_output,
                           player_scoreboard=player_scoreboard,
                           bot_scoreboard=bot_scoreboard,
                           game_ctrl_btn_c=html.Div(),
                           decision_ctrl_btn_c=html.Div(),
                           game_ctrl_btn_style=HIDDEN_BTN_STYLE,
                           decision_ctrl_btn_style=HIDDEN_BTN_STYLE,
                           player_table_block1_c=score_sheet_blocks['player-table-block1'],
                           player_table_block2_c=score_sheet_blocks['player-table-block2'],
                           bot_table_block1_c=score_sheet_blocks['bot-table-block1'],
                           bot_table_block2_c=score_sheet_blocks['bot-table-block2'],
                           game_ctrl_data={})
    
    
    else:
       
        if action_data['game-ctrl']['turn'] == 'player':
    
            # This will only be triggered on the first roll of a player's turn 
            # where the holdout set will be empty
            if action_exec_ctx['game-ctrl-btn'].triggered:                
                
                prior_holdout_dice, new_dice = utils.roll_dice(holdout=())
                roll_result = tuple(sorted(prior_holdout_dice + new_dice))    
                
                rolls_left = action_data['game-ctrl']['rolls-left'] - 1  
                
                player_scores, player_fills = fn_components.get_player_scores_x_fills(game_state)   
    
                roll_category_scores = {
                    cat: scoring.score_category(cat, roll_result, player_scores)
                    for cat in CATEGORIES
                }
    
                player_table_block1_c, player_table_block2_c = fn_components.generate_score_sheet_blocks(
                                                                       player=True,
                                                                       category_scores=roll_category_scores,
                                                                       current_fills=player_fills,
                                                                       current_scores=player_scores
                                                                )
                
                main_output = fn_components.generate_dice_output(roll_result, ())
    
                game_ctrl_btn_c = html.P("Show Bot Turn")
                
                decision_ctrl_btn_c = html.P(f"Select Action ({rolls_left} Rolls Left)") if rolls_left != 1 else html.P(f"Select Action ({rolls_left} Roll Left)")
                                             
                                             
                                             
                game_ctrl_data = fn_components.format_game_data(turn='player', 
                                             rolls_left=rolls_left, 
                                             player_block_1_score=action_data['game-ctrl']['player-block-1-score'], 
                                             player_block_2_score=action_data['game-ctrl']['player-block-2-score'], 
                                             bot_block_1_score=action_data['game-ctrl']['bot-block-1-score'],
                                             bot_block_2_score=action_data['game-ctrl']['bot-block-2-score'],
                                             game_over=False)
    
                
                player_scoreboard, bot_scoreboard = fn_components.format_scores(player_block_1_score=action_data['game-ctrl']['player-block-1-score'], 
                                                          player_block_2_score=action_data['game-ctrl']['player-block-2-score'],
                                                          bot_block_1_score=action_data['game-ctrl']['bot-block-1-score'], 
                                                          bot_block_2_score=action_data['game-ctrl']['bot-block-2-score'])
    
                return step_output(main_output=main_output,
                                   player_scoreboard=player_scoreboard,
                                   bot_scoreboard=bot_scoreboard,
                                   game_ctrl_btn_c=game_ctrl_btn_c,
                                   decision_ctrl_btn_c=decision_ctrl_btn_c,
                                   game_ctrl_btn_style=HIDDEN_BTN_STYLE,
                                   decision_ctrl_btn_style=ACTIVE_BTN_STYLE,
                                   player_table_block1_c=player_table_block1_c,
                                   player_table_block2_c=player_table_block2_c,
                                   bot_table_block1_c=score_sheet_blocks['bot-table-block1'],
                                   bot_table_block2_c=score_sheet_blocks['bot-table-block2'],
                                   game_ctrl_data=game_ctrl_data)
            
    
            # This will be triggered when the player submits their decision
            elif action_exec_ctx['decision-ctrl-btn'].triggered:
                
                decision = action_data['decision-ctrl']['decision']
    
                # if decision is to re-roll
                if isinstance(decision, list):
                    
                    prior_holdout_dice, new_dice = utils.roll_dice(holdout=action_data['decision-ctrl']['decision'])    
                    roll_result = tuple(sorted(prior_holdout_dice + new_dice))
    
                    rolls_left = action_data['game-ctrl']['rolls-left'] - 1
    
                    player_scores, player_fills = fn_components.get_player_scores_x_fills(game_state)            
                    
                    roll_category_scores = {
                        cat: scoring.score_category(cat, roll_result, player_scores)
                        for cat in CATEGORIES
                    }
    
                    player_table_block1_c, player_table_block2_c = fn_components.generate_score_sheet_blocks(
                                                                       player=True,
                                                                       category_scores=roll_category_scores,
                                                                       current_fills=player_fills,
                                                                       current_scores=player_scores
                                                                    )
    
                    main_output = fn_components.generate_dice_output(prior_holdout_dice, new_dice)    
    
                    game_ctrl_btn_c = html.P("Show Bot Turn")
                    decision_ctrl_btn_c = html.P(f"Select Action ({rolls_left} Rolls Left)") if rolls_left != 1 else html.P(f"Select Action ({rolls_left} Roll Left)")
                                                            
                
                    game_ctrl_data = fn_components.format_game_data(turn='player', 
                                                 rolls_left=rolls_left, 
                                                 player_block_1_score=action_data['game-ctrl']['player-block-1-score'], 
                                                 player_block_2_score=action_data['game-ctrl']['player-block-2-score'], 
                                                 bot_block_1_score=action_data['game-ctrl']['bot-block-1-score'],
                                                 bot_block_2_score=action_data['game-ctrl']['bot-block-2-score'],
                                                 game_over=False)
    
    
                    player_scoreboard, bot_scoreboard = fn_components.format_scores(player_block_1_score=action_data['game-ctrl']['player-block-1-score'], 
                                                              player_block_2_score=action_data['game-ctrl']['player-block-2-score'],
                                                              bot_block_1_score=action_data['game-ctrl']['bot-block-1-score'], 
                                                              bot_block_2_score=action_data['game-ctrl']['bot-block-2-score'])
                    
                    return step_output(main_output=main_output,
                                       player_scoreboard=player_scoreboard,
                                       bot_scoreboard=bot_scoreboard,
                                       game_ctrl_btn_c=game_ctrl_btn_c,
                                       decision_ctrl_btn_c=decision_ctrl_btn_c,
                                       game_ctrl_btn_style=HIDDEN_BTN_STYLE,
                                       decision_ctrl_btn_style=ACTIVE_BTN_STYLE,
                                       player_table_block1_c=player_table_block1_c,
                                       player_table_block2_c=player_table_block2_c,
                                       bot_table_block1_c=score_sheet_blocks['bot-table-block1'],
                                       bot_table_block2_c=score_sheet_blocks['bot-table-block2'],
                                       game_ctrl_data=game_ctrl_data)
    
            
                else:
    
                    player_scores, player_fills = fn_components.get_player_scores_x_fills(game_state)    
    
                    player_scores[decision] = scoring.score_category(decision, action_data['decision-ctrl']['dice'], player_scores)
                    player_fills[decision] = True
    
                    game_ctrl_btn_c = html.P("Show Bot Turn")
                    decision_ctrl_btn_c = html.P("Select Action ({} Rolls Left)".format(
                        action_data['game-ctrl']['rolls-left'] - 1    
                    ))
                        
                    player_block1_scores = sum([ v for k, v in player_scores.items() if k in BLOCK_1_CATEGORIES ])
                    player_block2_scores = sum([ v for k, v in player_scores.items() if k in BLOCK_2_CATEGORIES ])
                   
                    player_table_block1_c, player_table_block2_c = fn_components.generate_score_sheet_blocks(
                                                                       player=True,
                                                                       category_scores=player_scores,
                                                                       current_fills=player_fills,
                                                                       current_scores=player_scores
                                                                    )    
    
                    player_scoreboard, bot_scoreboard = fn_components.format_scores(player_block_1_score=player_block1_scores, 
                                                              player_block_2_score=player_block2_scores,
                                                              bot_block_1_score=action_data['game-ctrl']['bot-block-1-score'], 
                                                              bot_block_2_score=action_data['game-ctrl']['bot-block-2-score'])
    
                    game_ctrl_data = fn_components.format_game_data(turn='bot', 
                                                 rolls_left=None, 
                                                 player_block_1_score=player_block1_scores, 
                                                 player_block_2_score=player_block2_scores, 
                                                 bot_block_1_score=action_data['game-ctrl']['bot-block-1-score'],
                                                 bot_block_2_score=action_data['game-ctrl']['bot-block-2-score'],
                                                 game_over=False)    
    
                    return step_output(main_output=html.Div(),
                                       player_scoreboard=player_scoreboard,
                                       bot_scoreboard=bot_scoreboard,
                                       game_ctrl_btn_c=game_ctrl_btn_c,
                                       decision_ctrl_btn_c=decision_ctrl_btn_c,
                                       game_ctrl_btn_style=ACTIVE_BTN_STYLE,
                                       decision_ctrl_btn_style=HIDDEN_BTN_STYLE,
                                       player_table_block1_c=player_table_block1_c,
                                       player_table_block2_c=player_table_block2_c,
                                       bot_table_block1_c=score_sheet_blocks['bot-table-block1'],
                                       bot_table_block2_c=score_sheet_blocks['bot-table-block2'],
                                       game_ctrl_data=game_ctrl_data)
    
            else:
                raise dash.exceptions.PreventUpdate
    
        else:
    
            if action_exec_ctx['game-ctrl-btn'].triggered:
    
                yahtzee_bot = YahtzeeBot()
    
                turn_state_bot_scores, turn_start_bot_fills = fn_components.get_bot_scores_x_fills(game_state)
                
                turn_steps, turn_results = yahtzee_bot.play_turn(
                    fills=turn_start_bot_fills,
                    scores=turn_state_bot_scores
                )
                
                main_output_div_children = []
                for decision_dict in turn_steps: 
                    main_output_div_children.append(                    
                        fn_components.bot_decision_summary(decision_dict), 
                    )
                    
                main_output = html.Div(main_output_div_children, style={ 'display': 'flex', 
                                                      'justifyContent': 'center',
                                                      'flexDirection': 'column',
                                                      'width': '100%' }),
                        
                bot_fills = turn_results["fills"]
                bot_scores = turn_results["scores"]                
                
                is_game_over = all([ fill == True for fill in bot_fills.values() ])                
                
                bot_block1_scores = sum([ v for k, v in bot_scores.items() if k in BLOCK_1_CATEGORIES ])
                bot_block2_scores = sum([ v for k, v in bot_scores.items() if k in BLOCK_2_CATEGORIES ])
                                
                player_scoreboard, bot_scoreboard = fn_components.format_scores(player_block_1_score=action_data['game-ctrl']['player-block-1-score'], 
                                                          player_block_2_score=action_data['game-ctrl']['player-block-2-score'],
                                                          bot_block_1_score=bot_block1_scores, 
                                                          bot_block_2_score=bot_block2_scores)
                
                game_ctrl_btn_c = html.P("Start Turn") if not is_game_over else html.P("Finish Game!")
                decision_ctrl_btn_c = html.P("Select Action (3 Rolls Left)")
                            
                bot_table_block1_c, bot_table_block2_c = fn_components.generate_score_sheet_blocks(
                                                            player=False,
                                                            category_scores=bot_scores,
                                                            current_fills=bot_fills,
                                                            current_scores=bot_scores
                                                         )  
                     
                game_ctrl_data = fn_components.format_game_data(turn='player', 
                                             rolls_left=3, 
                                             player_block_1_score=action_data['game-ctrl']['player-block-1-score'], 
                                             player_block_2_score=action_data['game-ctrl']['player-block-2-score'], 
                                             bot_block_1_score=bot_block1_scores,
                                             bot_block_2_score=bot_block2_scores,
                                             game_over=is_game_over)
                                            
                return step_output(main_output=main_output,
                                   player_scoreboard=player_scoreboard,
                                   bot_scoreboard=bot_scoreboard,
                                   game_ctrl_btn_c=game_ctrl_btn_c,
                                   decision_ctrl_btn_c=decision_ctrl_btn_c,
                                   game_ctrl_btn_style=ACTIVE_BTN_STYLE,
                                   decision_ctrl_btn_style=HIDDEN_BTN_STYLE,
                                   player_table_block1_c=score_sheet_blocks['player-table-block1'],
                                   player_table_block2_c=score_sheet_blocks['player-table-block2'],
                                   bot_table_block1_c=bot_table_block1_c,
                                   bot_table_block2_c=bot_table_block2_c,
                                   game_ctrl_data=game_ctrl_data)
    
            else:
                raise dash.exceptions.PreventUpdate



@callback(
    [Output({'type': 'dice-btn', 'index': MATCH}, 'color'),
     Output({'type': 'dice-btn', 'index': MATCH}, 'disabled')],

    [Input({'type': 'dice-btn', 'index': MATCH}, 'n_clicks'),
     Input({'type': 'dice-btn', 'index': MATCH}, 'value'),
     State({'type': 'player-item', 'index': ALL}, 'color'),
     State('game-ctrl', 'data')],
)
def label_holdout(dice_btn, dice_value, item_colors, game_ctrl_data):

    if game_ctrl_data['rolls-left'] == 0:
        return 'dark', True
    else:
        if dice_btn:
            if dice_btn % 2 != 0 and all([c != 'success' for c in item_colors]):
                return 'success', False
            else:
                return 'dark', False
        else:
            raise dash.exceptions.PreventUpdate


@callback(
    Output({'type': 'player-item', 'index': MATCH}, 'color'),
    Output({'type': 'player-item', 'index': MATCH}, 'value'),

    [Input({'type': 'player-item', 'index': MATCH}, 'n_clicks'),
     State({'type': 'player-item', 'index': ALL}, 'color'),
     State({'type': 'dice-btn', 'index': ALL}, 'color')],
)
def label_category(player_item, item_colors, dice_colors):

    if player_item:
        if player_item % 2 != 0 and all([c != 'success' for c in item_colors]) and all([d != 'success' for d in dice_colors]):
            return 'success', 1
        else:
            return 'primary', 0
    else:
        raise dash.exceptions.PreventUpdate


@callback(
    Output('decision-ctrl', 'data'),
    Output('decision-ctrl-btn', 'disabled'),
    [
        Input({'type': 'player-item', 'index': ALL}, 'value'),
        Input({'type': 'dice-btn', 'index': ALL}, 'value'),
        Input({'type': 'dice-btn', 'index': ALL}, 'color'),
        State('game-ctrl', 'data')

    ],
)
# ALLOW EMPTY HOLDOUT
def update_decision_data(cat_vals, dice_vals, dice_selected, game_ctrl_data):
    
    if game_ctrl_data == {}:
        raise dash.exceptions.PreventUpdate
        
    else: 
        dice_data = list(zip(dice_vals, dice_selected))
    
        holdouts = []
        for d in dice_data:
            val, col = d
            if col == 'success':
                holdouts.append(val)
                
        holdouts = tuple(sorted(holdouts))
    
        category_map = dict(zip(CATEGORIES, cat_vals))
        category = ''.join([k for k, v in category_map.items() if v == 1])
    
        
        if game_ctrl_data['rolls-left'] == 0 and game_ctrl_data['turn'] == 'player' and category == "":
            return { "decision": None, "dice": tuple(sorted(dice_vals)) }, True
        
        else:     
            if category != '':
                return {"decision": category, "dice": tuple(sorted(dice_vals)) }, False
            else:
                return {"decision": holdouts, "dice": tuple(sorted(dice_vals)) }, False
                
            
    
@callback(
    Output("instructions", "is_open"),
    Input("open-instructions", "n_clicks"),
    [State("instructions", "is_open")],
)
def toggle_instructions(n1, is_open):
    if n1:
        return not is_open
    return is_open

                
        
def toggle_decision_logic(n1, is_open):
    if n1:
        return not is_open
    return is_open

        
callback(
    Output("modal-2", "is_open"),
    Input("open-modal-2", "n_clicks"),
    State("modal-2", "is_open"),
)(toggle_decision_logic)
       
 
callback(
    Output("modal-1", "is_open"),
    Input("open-modal-1", "n_clicks"),
    State("modal-1", "is_open"),
)(toggle_decision_logic)
       

callback(
    Output("modal-0", "is_open"),
    Input("open-modal-0", "n_clicks"),
    State("modal-0", "is_open"),
)(toggle_decision_logic)
       
        
        
        
        
        
