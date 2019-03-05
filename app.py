import arduino_helper
from pyfirmata import Arduino, util, STRING_DATA
import time
import random
import urllib.parse

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import datetime
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import scipy.integrate as integrate
from dash.dependencies import State, Input, Output
from constants import *
import temperature_graph
import control_panel

start_time = time.time()


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.config.suppress_callback_exceptions = True
connected = False

current_DC = 0.0

try:
    time.sleep(2)
    arduino_helper.update_duty_cycle(1.0)
    connected = True
except Exception as e:
    print(e)

header = html.Div(
    id="container",
    style={"background-color": "#119DFF"},
    children=[
        html.H2("Arduino Temperature Controller"),
    ],
    className="banner",
)
if not connected:
    header = html.Div(
        id="container",
        style={"background-color": "#119DFF"},
        children=[
            html.H2("Warning - not connected"),
        ],
        className="banner",
    )

app.layout = html.Div(
    [
        header,
        html.Div(
            [
                html.Div(
                    [
                        temperature_graph.layout
                    ],
                    className="row",
                    style={"marginTop": "3%"},
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                control_panel.layout
                                ],
                            className="eight columns",
                            style={
                                "border-radius": "5px",
                                "border-width": "5px",
                                "border": "1px solid rgb(216, 216, 216)",
                                "height": "434px",
                            },
                        ),
                        html.Div(
                            [
                                html.H3("Temperature", style={
                                        "textAlign": "center"}),
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
                                html.H3("Duty Cycle", style={
                                        "textAlign": "center"}),
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
                            ],
                            className="four columns",
                            style={
                                "border-radius": "5px",
                                "border-width": "5px",
                                "border": "1px solid rgb(216, 216, 216)",
                                "height": "436px",
                            },
                        ),
                    ],
                    className="row",
                ),
                html.Div(
                    [
                        html.Div(id=stop_time_id),
                        html.Div(id=start_time_id),
                        html.Div(id=reset_time_id),
                        html.Div(id="graph-data-send"),
                        html.Div(id=temperature_store_id),
                        html.Div(id=command_string),
                        html.Div(id="thermotype-hold"),
                        html.Div(id="filter-hold"),
                        html.Div(id="pid-action"),
                        html.Div(id="output-mode"),
                        html.Div(id=csv_string_id),
                        dcc.Interval(
                            id=graph_interval_id, interval=100000, n_intervals=0
                        ),
                    ],
                    style={"visibility": "hidden"},
                ),
            ],
            style={"padding": "0px 30px 0px 30px", },
        ),
    ],

    style={
        "padding": "0px 10px 0px 10px",
        "marginLeft": "auto",
        "marginRight": "auto",
        "width": "1180px",
        "height": "955px",
        "boxShadow": "0px 0px 5px 5px rgba(204,204,204,0.4)",
    },
)

# Buttons

@app.callback(
    Output(start_time_id, "children"),
    [Input(start_button_id, "n_clicks")]
)
def start_time(start):
    if start > 0:
        return time.time()
    return 0


@app.callback(
    Output(stop_time_id, "children"),
    [Input(stop_button_id, "n_clicks")]
)
def stop_time(stop):
    if stop > 0:
        return time.time()
    return 0


@app.callback(
    Output(download_link_id, "href"),
    [Input(download_button_id, "n_clicks")],
    [State(csv_string_id, "value")]
)
def download(clicks, csvString):
    return "data:text/csv;charset=utf-8," + urllib.parse.quote(csvString)


@app.callback(
    Output(reset_time_id, "children"),
    [Input(reset_button_id, "n_clicks")]
)
def reset_time(reset):
    return time.time()

# Button Control Panel

@app.callback(
    Output(command_string, "children"),
    [Input(start_time_id, "children"),
     Input(stop_time_id, "children"),
     Input(reset_time_id, "children")]
)
def command_string_button(
    start_button,
    stop_button,
    reset_button
):
    master_command = {
        "START": start_button,
        "STOP": stop_button,
        "RESET": reset_button,
    }
    recent_command = max(master_command, key=master_command.get)
    return recent_command


# Rate
@app.callback(
    Output(graph_interval_id, "interval"),
    [Input(command_string, "children"),
     Input(refresh_rate_id, "value")],
)
def graph_control(command, rate):
    if command == "START":
        rate = int(rate) * 1000
        return rate
    else:
        return 3000

@app.callback(
    Output(derivative_time_id, "value"),
    [Input(dead_time_switch_id, "on")]
)
def dead_time_dev_gain_value(switch):
    if switch:
        return 0.1
    return 0


@app.callback(
    Output(conroller_gain_id, "value"),
    [Input(dead_time_switch_id, "on")]
)
def dead_time_dev_gain_value(switch):
    if switch:
        return 0.26
    return 0.44


@app.callback(
    Output(integral_time_id, "value"),
    [Input(dead_time_switch_id, "on")]
)
def dead_time_dev_gain_value(switch):
    if switch:
        return 100
    return 35


@app.callback(
    Output(derivative_time_id, "disabled"),
    [Input(dead_time_switch_id, "on")]
)
def dead_time_dev_gain_value(switch):
    derivative_time_disabled = not switch
    return derivative_time_disabled


@app.callback(
    Output(setpoint_id, "max"),
    [Input(dead_time_switch_id, "on")]
)
def dead_time(dead_time_on):
    if dead_time_on:
        return 32
    return 42

@app.callback(
    Output(temperature_store_id, "children"),
    [Input(command_string, "children"),
     Input(graph_interval_id, "n_intervals")],
)
def get_new_temperature(command, rate):
    if command == "START":
        return arduino_helper.get_temperature()

@app.callback(
    Output(temperature_display_id, "value"),
    [Input(graph_interval_id, "n_intervals")],
    [State(temperature_store_id, "children"),
     State(command_string, "children")],
)
def get_temperature_for_display(interval, temperature, command):
    if command == "START":
        temperature = "%.2f" % temperature
        return temperature
    else:
        return "25.00"

@app.callback(
    Output(duty_cycle_id, "value"),
    [Input(graph_interval_id, "n_intervals")],
    [State(refresh_rate_id, "value"),
     State(duty_cycle_id, "value"),
     State(command_string, "children"),
     State(setpoint_id, "value"),
     State(temperature_store_id, "children"),
     State(derivative_time_id, "value"),
     State(conroller_gain_id, "value"),
     State(integral_time_id, "value")]
)
def get_new_dc(interval, rate, current_DC, command, PID_setpoint, temperature, dev_gain, pro_gain, int_gain):
    if command == "START":
        EN_previous = PID_setpoint - temperature
        EN_current = PID_setpoint - temperature

        PID_setpoint = float(PID_setpoint)
        PID_setpoint = str(PID_setpoint)

        delta_time = rate
        int_gain = float(int_gain)
        pro_gain = float(pro_gain)
        current_DC = float(current_DC)
        current_DC += pro_gain * \
            (EN_current - EN_previous + (delta_time/int_gain) * EN_current)
        if current_DC > 1:
            current_DC = 1
        if current_DC < 0:
            current_DC = 0
        arduino_helper.update_duty_cycle(current_DC)
        return "%.2f" % current_DC

    arduino_helper.update_duty_cycle(0)
    return "0.00"

@app.callback(
    Output(csv_string_id, "value"),
    [Input(temperature_store_id, "children")],
    [State(csv_string_id, "value"),
     State(command_string, "children"),
     State(duty_cycle_id, "value"),
     State(setpoint_id, "value"),
     State(derivative_time_id, "value"),
     State(conroller_gain_id, "value"),
     State(integral_time_id, "value")],
)
def log_to_csv(temperature, data, command, duty_cycle, setpoint, dev_gain, pro_gain, int_gain):
    if not data:
        data = "time,temperature,duty cycle,set point,dev gain,controller gain,integral gain\n"
    if command != "START":
        return
    time_now = datetime.datetime.now().strftime("%H:%M:%S")
    new_row = f"{time_now},{temperature},{duty_cycle},{setpoint},{dev_gain},{pro_gain},{int_gain}"
    data += new_row + "\n"


@app.callback(
    Output(graph_data_id, "figure"),
    [Input(temperature_store_id, "children")],
    [State(graph_data_id, "figure"),
     State(command_string, "children"),
     State(start_time_id, "children"),
     State(start_button_id, "n_clicks"),
     State(setpoint_id, "value"),
     State(duty_cycle_id, "value")],
)
def graph_data(temperature, figure, command, start, start_button, PID, duty_cycle):
    print("command: ", command)
    if command == "START":
        times = figure["data"][0]["x"]
        temperatures = figure["data"][0]["y"]
        set_points = figure["data"][1]["y"]
        duty_cycles = figure["data"][2]["y"]
        times.append(time.time() - float(start))
        temperatures.append(temperature)
        set_points.append(PID)
        duty_cycles.append(float(duty_cycle))
    elif command == "RESET":
        times = []
        temperatures = []
        set_points = []
        duty_cycles = []
        time_now = 0
    else:
        times = figure["data"][0]["x"]
        temperatures = figure["data"][0]["y"]
        set_points = figure["data"][1]["y"]
        duty_cycles = figure["data"][2]["y"]
    return {
        "data": [
            go.Scatter(
                x=times,
                y=temperatures,
                mode="lines",
                marker={"size": 6},
                name="Temperature (°C)"
            ),
            go.Scatter(
                x=times,
                y=set_points,
                mode="lines",
                marker={"size": 6},
                name="Set Point (°C)",
            ),
            go.Scatter(
                x=times,
                y=duty_cycles,
                mode="lines",
                marker={"size": 6},
                name="Duty Cycle",
                visible=False
            ),
        ],
        "layout": go.Layout(
            autosize=True,
            showlegend=True,
            xaxis={"title": "Time (s)", "autorange": True},
            yaxis={"title": "Temperature(°C)", "autorange": True},
            # yaxis2={"title": "Duty Cycle", "autorange": True, "side": "right"},
            margin={"l": 70, "b": 100, "t": 0, "r": 25},
        ),
    }


if __name__ == '__main__':
    with open('requirements.txt') as f:
        required = f.read().splitlines()
    app.run_server(debug=False)
