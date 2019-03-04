from constants import *

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import plotly.graph_objs as go

layout = html.Div([
    html.H3("Control Panel", style={"textAlign": "center", "paddingBottom": "3%", }),
    html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            daq.StopButton(
                                id=start_button_id,
                                buttonText="Start",
                                style={
                                    "display": "flex",
                                    "justify-content": "center",
                                    "align-items": "center",
                                    "paddingBottom": "25%",
                                },
                                n_clicks=0,
                            ),
                            daq.StopButton(
                                id=stop_button_id,
                                buttonText="Stop",
                                style={
                                    "display": "flex",
                                    "justify-content": "center",
                                    "align-items": "center",
                                    "paddingBottom": "25%",
                                },
                                n_clicks=0,
                            ),
                            daq.StopButton(
                                id=reset_button_id,
                                buttonText="Reset",
                                style={
                                    "display": "flex",
                                    "justify-content": "center",
                                    "align-items": "center",
                                    "paddingBottom": "25%",
                                },
                                n_clicks=0,
                            ),
                        ],
                        className="four columns",
                        style={"marginLeft": "5%"},
                    ),
                    html.Div(
                        [
                            daq.NumericInput(
                                id=refresh_rate_id,
                                label="Refresh Rate (s)",
                                labelPosition="bottom",
                                size=75,
                                value=3,
                                max=10,
                                style={
                                    "display": "flex",
                                    "justify-content": "center",
                                    "align-items": "center",
                                    "paddingBottom": "25%",
                                },
                            ),
                            daq.NumericInput(
                                id=setpoint_id,
                                label="PID Setpoint (°C)",
                                value=26,
                                max=35,
                                min=25,
                                size=75,
                                labelPosition="bottom",
                                style={
                                    "display": "flex",
                                    "justify-content": "center",
                                    "align-items": "center",
                                    "paddingBottom": "15%",
                                },
                            ),
                            daq.BooleanSwitch(
                                id=dead_time_switch_id,
                                label="Dead Time",
                                labelPosition="bottom",
                                on=False,
                                style={
                                    "display": "flex",
                                    "justify-content": "center",
                                    "align-items": "center",
                                    "paddingBottom": "15%",
                                },
                            ),
                        ],
                        className="three columns",
                        style={"marginLeft": "5%"},
                    ),
                    html.Div(
                        [
                            daq.NumericInput(
                                id=conroller_gain_id,
                                label="Controller Gain",
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
                                label="Integral Time",
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
                            daq.NumericInput(
                                id=derivative_time_id,
                                label="Derivative Time",
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
                       className="three columns", 
                       style={"marginLeft": "5%"},
                    )
                ],
            ),
        ]
    )
]
)
