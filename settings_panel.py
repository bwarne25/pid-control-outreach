from constants import *
import time
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import plotly.graph_objs as go

layout = html.Div([
    html.H3("Settings", style={
            "textAlign": "center", "paddingBottom": "3%", }),
    html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            daq.NumericInput(
                                id=refresh_rate_id,
                                label="Refresh Rate (s)",
                                labelPosition="bottom",
                                size=75,
                                value=3,
                                max=10,
                            ),
                        ],
                        className="three columns", 
                       style={"marginLeft": "5%"},
                    ),
                    html.Div(
                        [
                            daq.BooleanSwitch(
                                id=dead_time_switch_id,
                                label="Dead Time",
                                labelPosition="bottom",
                                on=False,
                            ),
                        ],
                        className="three columns", 
                       style={"marginLeft": "5%"},
                       ),
                    html.Div(
                        [
                            dcc.Input(
                                id=port_name_id,
                                type='text',
                                value='COM5'
                                ),
                            html.P("Port")
                        ],
                        className="three columns", 
                       style={"marginLeft": "5%"},
                    ),
                    html.Div([daq.Indicator(
                        id=is_connected,
                        label="Connected",
                        labelPosition="bottom",
                        value=True
                    )])
                ],
                className="row",
                style={"marginLeft": "5%"},
            ),
        ],
        
    ),
]
)
