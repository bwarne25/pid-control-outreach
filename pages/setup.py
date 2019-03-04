import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_daq as daq
import random

from app import app
from pages import main_graph

layout = html.Div([
    html.H3('Setup'),
    html.Div(
        [
            html.Div(
                            [
                                html.H3(
                                    "Test", 
                                    style={"textAlign": "center"}),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                        daq.StopButton(
                                                            id="test-button",
                                                            buttonText="Test",
                                                            style={
                                                                "display": "flex",
                                                                "justify-content": "center",
                                                                "align-items": "center",
                                                                "paddingBottom": "22%",
                                                            },
                                                            n_clicks=0,
                                                        ),
                                                    ],
                                                    
                                                    className="three columns",
                                                    style={"marginLeft": "13%"},
                                                ),
                                                html.Div([                                        
                                            daq.Indicator(
                                            id="success-indicator",
                                            label="",
                                            value=True,
                                            color="#00cc96",
                                            className="one columns",
                                            labelPosition="top",
                                            style={
                                                "position": "absolute",
                                                "left": "20%",
                                                "top": "33%"      
                                            },
                                        ),])
                                            ],
                                            className="row",
                                        )
                                    ]
                                ),
                            ],
                            className="six columns",
                            style={
                                "border-radius": "5px",
                                "border-width": "5px",
                                "border": "1px solid rgb(216, 216, 216)",
                                "height": "434px",
                            },
            )
        ],
        style={"height": "100%"})],
     style={
        "padding": "0px 10px 0px 10px",
        "marginLeft": "auto",
        "marginRight": "auto",
        "width": "1180px",
        "height": "955px",
        "boxShadow": "0px 0px 5px 5px rgba(204,204,204,0.4)",
    },
)

@app.callback(
    Output("success-indicator", "color"), 
    [Input("test-button", "n_clicks")]
)
def test(test):
    return random.choice(["#00cc96", "#EF553B"])
