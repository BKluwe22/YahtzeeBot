import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State, callback, ALL, MATCH
import warnings
import requests
import dash_tabulator
import fn_components
import plotly.express as px 
import pandas as pd 
import math

warnings.filterwarnings("ignore")

CATEGORIES = ["ones", "twos", "threes", "fours", "fives", "sixes",
              "three-of-a-kind", "four-of-a-kind", "full-house",
              "small-straight", "large-straight", "yahtzee",
              "chance"]

BLOCK_1_CATEGORIES = ["ones", "twos", "threes", "fours", "fives", "sixes"]
BLOCK_2_CATEGORIES = ["three-of-a-kind", "four-of-a-kind", "full-house",
                      "small-straight", "large-straight", "yahtzee",
                      "chance"]

DICE_NUM_MAP = {
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six"
}


CATEGORY_OPTION_MAP = {

    "ones": [i for i in range(6)],
    "twos": [i*2 for i in range(6)],
    "threes": [i*3 for i in range(6)],
    "fours": [i*4 for i in range(6)],
    "fives": [i*5 for i in range(6)],
    "sixes": [i*6 for i in range(6)],

    "three-of-a-kind": [0, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                        21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 100],

    "four-of-a-kind": [0, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                       21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 100],

    "full-house": [0, 25, 100],
    "small-straight": [0, 30, 100],
    "large-straight": [0, 40, 100],
    "yahtzee": [0, 50, 100],
    "chance":  [0, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 100]
}


def dice(id_num):

    return html.Div([
        html.Div([

            dcc.Store(id={'type': 'dice-value', 'index': id_num},
                      data={'value': id_num}),
            html.H1(id={'type': 'dice-children', 'index': id_num},
                    children=html.I(className=f"bi bi-dice-{id_num}")),

            dbc.ButtonGroup([

                dbc.Button([html.I(className="bi bi-arrow-down-circle")],
                           id={'type': 'dice-down', 'index': id_num},
                           n_clicks=0,
                           outline=True,
                           color="dark",
                           size="sm"),

                dbc.Button([html.I(className="bi bi-arrow-up-circle")],
                           id={'type': 'dice-up', 'index': id_num},
                           n_clicks=0,
                           outline=True,
                           color="dark",
                           size="sm")

            ])
        ], style={'display': 'flex',
                  'rowGap': '2.5%',
                  'flexDirection': 'column',
                  'justifyContent': 'center',
                  'alignItems': 'center'}),
    ])


dash.register_page(__name__, path="/dashboard")


def score_sheet_row(category: str):

    return html.Tr([

        html.P(category.title(), style={'textAlign': 'center'}),

        html.Td([
            html.Div([
                dcc.Dropdown(
                    id={"type": "score", "index": category},
                    value=0,
                    placeholder="Select Value",
                    style={'width': '75%'},
                    options=[{'label': i, 'value': i}
                             for i in CATEGORY_OPTION_MAP[category]]
                ),

                dbc.Switch(
                    id={"type": "fill", "index": category},
                    label="Filled",
                    value=False,
                )
            ], style={
                'display': 'flex',
                'justifyContent': 'space-around',
                'flexDirection': 'rows',
            })
        ], style={'width': '75%'})

    ])


score_sheet = dbc.Table(children=[

    html.Thead(
        html.Tr([
            html.Th("Category", style={
                    'fontSize': 'small', 'textAlign': 'center'}),
            html.Th("Data", style={
                    'fontSize': 'small', 'textAlign': 'center'})
        ])
    ),
    html.Tbody(id='score-sheet', children=[
        score_sheet_row(category=cat)
        for cat in CATEGORIES
    ]),

], bordered=True, size="sm")


layout = dbc.Container([

    html.Div([
        html.Div([
            html.Div([
                dice(1), dice(2), dice(3), dice(4), dice(5)
            ], style={
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "space-evenly"
            }),

            html.Br(),

            html.Div([
                html.Label("Rolls Left", htmlFor='rolls-left'),
                dcc.Dropdown(
                    id='rolls-left',
                    options=[{"label": i, "value": i} for i in range(3)],
                    value=2
                )
            ], style={
                'width': '75%',
                'justifyContent': 'center',
                'marginLeft': 'auto',
                'marginRight': 'auto'
            }),

            html.Br(),

            score_sheet,

            html.Br(),

            dbc.Button("Analyze State", id='submit-state'),
            html.Br(),
            html.Br(),

        ], style={
            'width': '40%',
            'display': 'flex',
            'flexDirection': 'column',
        }),

      html.Div(id='analytics', style={
          'width': '60%',
          'display': 'flex',
          'flexDirection': 'column',
          'justifyContent': 'space-evenly'
      })
            
   ], style = {
       'display': 'flex',    
       'flexDirection': 'row',
   }),
       
   html.Br(),
   html.Br(),
   html.Br(),
   html.Br(),

   html.Div([
       html.Div(id='simulation-selection'),
       html.Br(),
       html.Br(),
       html.Br(),
       html.Br(),
       html.Br(),
       html.Br(),
       dbc.Spinner(dbc.Col([
            html.Div(id='simulation-results')
       ]), color="primary", spinner_style={"width": "3rem", "height": "3rem"}),
   
   ])
   


], fluid=True, style={
    'marginTop': '1%',
})



@callback(
    [
        Output({'type': 'dice-children', 'index': MATCH}, 'children'),
        Output({'type': 'dice-up', 'index': MATCH}, 'disabled'),
        Output({'type': 'dice-down', 'index': MATCH}, 'disabled'),
        Output({'type': 'dice-value', 'index': MATCH}, 'data'),
    ],

    [
        Input({'type': 'dice-up', 'index': MATCH}, 'n_clicks'),
        Input({'type': 'dice-down', 'index': MATCH}, 'n_clicks'),
    ]
)
def update_dice(up_clicks, down_clicks):

    current_dice_number = 1 + (up_clicks - down_clicks)

    if (up_clicks - down_clicks) == 5:
        return html.I(className="bi bi-dice-6"), True, False, {"value": 6}

    elif (up_clicks - down_clicks) == 0:
        return html.I(className="bi bi-dice-1"), False, True, {"value": 1}

    else:
        return html.I(className=f"bi bi-dice-{current_dice_number}"), False, False, {"value": current_dice_number}


@callback(
    Output({"type": 'fill', 'index': MATCH}, 'value'),
    
    [
        Input({"type": 'score', 'index': MATCH}, 'value'),
        Input({"type": 'fill', 'index': MATCH}, 'value'),
    ]
)
def update_score_sheet(val, fill):

    if val == None:
        return False

    else:
        if fill == True:
            return True

        elif fill == False and val != 0:
            return True

        else:
            return False


@callback(
    [
     Output('analytics', 'children'),
     Output('simulation-selection', 'children')
    ],
    [
     Input('submit-state', 'n_clicks'),
     State({ 'type': 'dice-value', 'index': ALL }, 'data'),
     State("rolls-left", 'value'),
     State({ 'type': 'score', 'index': ALL }, "value"),
     State({ 'type': 'fill', 'index': ALL }, "value")
    ]

)
def show_analytics(n_clicks,
                    dice,
                    rolls_left,
                    scores,
                    fills
                   ):
    
    fills = dict(zip(CATEGORIES, fills))
    scores = dict(zip(CATEGORIES, scores))

    if n_clicks:

        dice = tuple(sorted([ x['value'] for x in dice ]))        
        
        action_distribution_fig, action_distribution = fn_components.action_values_relative_to_ev(dice,
                                                                                                  rolls_left,
                                                                                                  scores,
                                                                                                  fills, 
                                                                                                  450)


        action_probability_fig, action_probabilities = fn_components.action_value_probabilities(dice,
                                                                                                rolls_left,
                                                                                                scores,
                                                                                                fills, 
                                                                                                450)


        simulation_selection = html.Div([
            
            fn_components.simulation_candidates(dice, rolls_left, scores, fills),
            
            html.Div([
                dcc.Slider(1, 10000, 99,
                           value=1000,
                           marks={
                               i: { 'label': str(i) } for i in range(0, 10001, 1000)
                           },
                           id='simulation-num-slider'
                ),
                html.Div(id='simulation-num-output')   
            ], style={ 'width': '75%', 'marginLeft': 'auto', 'marginRight': 'auto '}),            
            
            html.Br(),
            html.Br(), 
            
            html.Div([
                
                dbc.Button("Simulate Actions", 
                            id="simulation-submission-btn",
                           outline=True,
                           color="primary",
                           className="me-1"),
                    
            ], style={ "display": "flex", "justifyContent": "center", "alignItems": "center" }),
            
        
        ]),
        
        
        analytics_output = html.Div([
            
            dcc.Graph(figure=action_distribution_fig),
            html.Br(),
            dcc.Graph(figure=action_probability_fig)
            
        ], style = {
            'width': '90%',    
            'marginLeft': 'auto',
            'marginRight': 'auto'
        })
            
        return analytics_output, simulation_selection

    else:
        return html.Div(), html.Div()




@callback(
    Output('simulation-num-output', 'children'),
    Input('simulation-num-slider', 'value'))

def update_output(value):
    return f'Run {value} parallel simulations'





@callback(
    Output('simulation-results', 'children'),
    [
     Input('simulation-submission-btn', 'n_clicks'),
     State('holdout-simulation-switches', 'value'),
     State('category-simulation-switches', 'value'),
     
     State({ 'type': 'dice-value', 'index': ALL }, 'data'),
     State("rolls-left", 'value'),
     State({ 'type': 'score', 'index': ALL }, "value"),
     State({ 'type': 'fill', 'index': ALL }, "value"),
     State('simulation-num-slider', 'value')
    ]
)




def simulate_actions(n_clicks, 
                     holdout_simulations, 
                     category_simulations,
                     dice, 
                     rolls_left, 
                     scores, 
                     fills,
                     n_simulations
    ):
    print(n_simulations)
    
    fills = dict(zip(CATEGORIES, fills))
    scores = dict(zip(CATEGORIES, scores))
    dice = tuple(sorted([ x['value'] for x in dice ]))        

    if n_clicks and n_simulations != 0:

        holdout_simulations = [ tuple(sorted(x)) for x in holdout_simulations]
        simulation_actions = category_simulations + holdout_simulations

        res = requests.post('http://simulation_server:5000/simulate',
                            json={
                                "dice": dice,
                                "rolls_left": rolls_left,
                                "scores": scores,
                                "fills": fills,
                                "n_simulations": n_simulations,
                                "simulation_actions": simulation_actions
                            }
        )
        if res.ok:
            simulation_res = res.json()
            
            columns = [
                { "title": "Action", "field": "action" },
                { "title": "N", "field": "n_observations" },
                { "title": "Mean", "field": "mean" },
                { "title": "Median", "field": "median" },
                { "title": "Min", "field": "min" },
                { "title": "Max", "field": "max" },
                { "title": "Skew", "field": "skew" },
                { "title": "Kurtosis", "field": "kurtosis" }
            ]

            if simulation_res != []:                
                
                df = pd.DataFrame(simulation_res)
                df['action'] = df['action'].astype(str)

                score_df = df[['action', 'scores']]
                score_df = score_df.explode('scores').reset_index(drop=True)

                stat_df = df.drop(['scores'], axis=1)

                fig = px.histogram(
                            score_df, x='scores', 
                            facet_col='action',
                            facet_col_wrap=2,
                            facet_row_spacing=0.2,
                            template='simple_white',
                            height=math.ceil(len(simulation_actions)/2)*400
                )
                
                fig.update_xaxes(showticklabels=True)


                return html.Div([

                            html.Br(),
                            html.H3("Simulation Results", style={'textAlign': 'center'}),
                            html.Br(),
                            html.Br(),
                            
                            dash_tabulator.DashTabulator(
                                    id='simulation-result-table',
                                    columns=columns,
                                    data=stat_df.to_dict(orient='records')
                            ),
                            
                            html.Br(),
                            html.Br(),
                            
                            dcc.Graph(id='simulation-result-histograms', figure=fig),                         
                            
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),

                        ], style={ 'width': '75%',
                                    'margin-left': 'auto',
                                    'margin-right': 'auto',
                })
            else:
                return html.Div()

        else:

            return html.Div(html.P("ERROR"))
        
    else: 
        return html.Div()
