import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_daq as daq

from app import app

from pages import main_graph, setup


layout = html.Div(
    dcc.Tabs(id="tabs", children=[
        dcc.Tab(label='Home', children=[
            html.Iframe(src='https://dash.plot.ly/dash-core-components',
                                             style={
                                                "width": "100%",
                                                "height":"100%",
                                                "boarder": "none",
                                                "position": "absolute"
                                            })
        ],
        ),
        dcc.Tab(label='Graph', children = main_graph.layout)],
        )
)
