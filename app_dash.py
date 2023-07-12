import dash as d
from dash import Dash, html, dcc, callback, Output, Input, State
import dash_player as dp
import plotly.express as px
import pandas as pd

import requests
import json



BACKEND_URL="http://127.0.0.1:8000"


def create_dash_app(requests_pathname_prefix: str = None) -> d.Dash:

    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

    # server = flask.Flask(__name__)

    app = d.Dash(__name__, requests_pathname_prefix=requests_pathname_prefix)
    app.scripts.config.serve_locally = False
    dcc._js_dist[0]['external_url'] = 'https://cdn.plot.ly/plotly-basic-latest.min.js'



    app.layout = html.Div(
        [
            # html.Div(
            #     style={"width": "48%", "padding": "0px"},
            #     children=[
            #         dp.DashPlayer(
            #             id="player",
            #             # url="https://youtu.be/d5pb9TgCGc0",
            #             url=d.get_asset_url("./pexels-camila-flores-16883440 (1080p).mp4"),
            #             controls=True,
            #             width="100%",
            #             height="250px",
            #         ),
            #     ]
            # ),

            html.Div(
                style={'max-width':'640px'},
                children = [
                    html.Video(
                        id="video-player",
                        controls=True,
                        src=d.get_asset_url("./pexels-camila-flores-16883440 (1080p).mp4"),
                        width='100%'
                    ),
                ]
            ),

            html.H6("更 "),
            html.Div(["输入：",
                    dcc.Input(id='my-input', value='初始值', type='text')]),
            html.Br(),
            html.Div(id='my-output'),

            html.H1(children='Title of Dash App', style={'textAlign':'center'}),
            dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection'),
            dcc.Graph(id='graph-content'),

            dcc.Store(id='count', data=0),

            html.Div([
                html.Div(dcc.Input(id='input-on-submit', type='number')),
                html.Button('Submit', id='submit-val', n_clicks=0),
                html.Div(id='container-button-basic', children='Enter a value and press submit')
            ])
        ]
    )



    @app.callback(
        Output('graph-content', 'figure'),
        Input('dropdown-selection', 'value')
    )
    def update_graph(value):
        dff = df[df.country==value]
        return px.line(dff, x='year', y='pop')


    @app.callback(
        Output(component_id='my-output', component_property='children'),
        Output('count', 'data'),

        Input(component_id='my-input', component_property='value'),
        Input('count', 'data'),
    )
    def update_output_div(value_in, data_in):
        if data_in % 2 == 0:
            res = requests.get(f'{BACKEND_URL}/status')
        else:
            res = requests.get(f'{BACKEND_URL}/st')
        
        message = json.loads(res.content)
        message = str(message)

        data_in += 1

        return message, data_in


    @app.callback(
        Output('container-button-basic', 'children'),
        Input('submit-val', 'n_clicks'),
        State('input-on-submit', 'value')
    )
    def update_output(n_clicks, value):
        return 'The input value was "{}" and the button has been clicked {} times'.format(
            value,
            n_clicks
        )



    return app
