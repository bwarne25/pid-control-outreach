from constants import *

import dash
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

layout = html.Div(
    [
        html.Div(
            [
                html.H4(
                    "Temperature vs. Time",
                    # className=" three columns card-title",
                ),
                 daq.StopButton(
                                id=export_button_id,
                                buttonText="Export",
                                n_clicks=0,
                                disabled=False
                            ),
            ],
            # className="row",
        ),
        dcc.Graph(
            id=graph_data_id,
            figure={
                "data": [
                    go.Scatter(
                        x=[],
                        y=[],
                        mode="markers",
                        marker={"size": 6},
                        name="Temperature (C°)",
                    ),
                    go.Scatter(
                        x=[],
                        y=[],
                        mode="lines",
                        marker={"size": 6},
                        name="Set Point (°C)",
                    ),
                    go.Scatter(
                        x=[],
                        y=[],
                        mode="lines",
                        marker={"size": 6},
                        name="dev)",
                    ),
                    go.Scatter(
                        x=[],
                        y=[],
                        mode="lines",
                        marker={"size": 6},
                        name="pro",
                    ),
                    go.Scatter(
                        x=[],
                        y=[],
                        mode="lines",
                        marker={"size": 6},
                        name="int",
                    )
                ],
                "layout": go.Layout(
                    xaxis={
                        "title": "Time (s)",
                        "autorange": True,
                    },
                    yaxis={
                        "title": "Temperature (°C)", "autorange": True},
                    margin={"l": 70, "b": 100,
                            "t": 0, "r": 25},
                ),
            },
        ),
    ],
)
