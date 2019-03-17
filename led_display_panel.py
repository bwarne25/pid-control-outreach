from constants import *
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq

layout = html.Div([html.H3("Temperature", className="card-title"),
    html.Div(
    [
        daq.LEDDisplay(
            id=temperature_display_id,
            value="25.00",
            style={
                "display": "flex",
                "justify-content": "center",
                "align-items": "center",
                "paddingTop": "1.7%",
                "paddingLeft": "20.5%",
                "marginLeft": "-7%",
                "marginRight": "2%",
            },
            className="eight columns",
            size=36,
        ),
        html.Div(
            children=[
                html.H5(
                    "°C",
                    style={
                        "border-radius": "3px",
                        "border-width": "5px",
                        "border": "1px solid rgb(216, 216, 216)",
                        "font-size": "47px",
                        "color": "#2a3f5f",
                        "display": "flex",
                        "justify-content": "center",
                        "align-items": "center",
                        "width": "27%",
                        "marginLeft": "3%",
                    },
                    className="four columns",
                )
            ],
        ),
    ],
    className="row",
    style={"marginBottom": "2%"},
),
    html.H3("Duty Cycle", className="card-title"),
    html.Div(
    [
        daq.LEDDisplay(
            id=duty_cycle_id,
            value="0.00",
            style={
                "display": "flex",
                "justify-content": "center",
                "align-items": "center",
                "paddingTop": "1.7%",
                "paddingLeft": "20.5%",
                "marginLeft": "-7%",
                "marginRight": "2%",
            },
            className="eight columns",
            size=36,
        ),
        html.Div(
            children=[
                html.H5(
                    "DC",
                    style={
                        "border-radius": "3px",
                        "border-width": "5px",
                        "border": "1px solid rgb(216, 216, 216)",
                        "font-size": "47px",
                        "color": "#2a3f5f",
                        "display": "flex",
                        "justify-content": "center",
                        "align-items": "center",
                        "width": "27%",
                        "marginLeft": "3%",
                    },
                    className="four columns",
                )
            ],
        ),
    ],
    className="row",
    style={"marginBottom": "2%"},
),
])
