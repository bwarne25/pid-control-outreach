from constants import *
import time
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import plotly.graph_objs as go

layout = html.Div([
    html.H3("Control Panel", className="card-title"),
    html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            daq.StopButton(
                                id=start_button_id,
                                buttonText="Start",
                                className="control-button",
                                n_clicks=0,
                                disabled=False
                            ),
                            daq.StopButton(
                                id=stop_button_id,
                                buttonText="Stop",
                                className="control-button",
                                n_clicks=0,
                                disabled=True
                            ),
                            daq.StopButton(
                                id=reset_button_id,
                                buttonText="Reset",
                                className="control-button",
                                n_clicks=0,
                                disabled=True
                            ),
                        ],
                        # className="four columns",
                        style={"marginLeft": "5%"},
                    ),
                    html.Div(
                        [
                            daq.NumericInput(
                                id=setpoint_id,
                                label="PID Setpoint (°C)",
                                value=30,
                                max=50,
                                min=20,
                                size=75,
                                labelPosition="bottom",
                                style={
                                    "display": "flex",
                                    "justify-content": "center",
                                    "align-items": "center",
                                    "paddingBottom": "15%",
                                },
                            ),
                            daq.NumericInput(
                                id=derivative_time_id,
                                label="Derivative Time (s)",
                                value=0.1,
                                max=1,
                                min=0,
                                size=75,
                                labelPosition="bottom",
                                disabled=False,
                                style={
                                    "display": "flex",
                                    "justify-content": "center",
                                    "align-items": "center",
                                    "paddingBottom": "15%",
                                },
                            )
                        ],
                        # className="three columns",
                        style={"marginLeft": "5%"},
                    ),
                    html.Div(
                        [
                            daq.NumericInput(
                                id=conroller_gain_id,
                                label="Controller Gain (DC/°C)",
                                value=0.44,
                                max=5,
                                min=0,
                                size=75,
                                labelPosition="bottom",
                                disabled=False,
                                style={
                                    "display": "flex",
                                    "justify-content": "center",
                                    "align-items": "center",
                                    "paddingBottom": "15%",
                                },
                            ),
                            daq.NumericInput(
                                id=integral_time_id,
                                label="Integral Time (s)",
                                value=35.00,
                                max=300,
                                min=0,
                                size=75,
                                labelPosition="bottom",
                                disabled=False,
                                style={
                                    "display": "flex",
                                    "justify-content": "center",
                                    "align-items": "center",
                                    "paddingBottom": "15%",
                                },
                            ),

                        ],
                    #    className="three columns", 
                       style={"marginLeft": "5%"},
                    )
                ],
            ),
        ]
    )
]
)

