import arduino_helper
from pyfirmata import Arduino, util, STRING_DATA
import time
import random
import urllib.parse
import os
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
import settings_panel
import led_display_panel
from command_state import CommandState
import threading
import webbrowser

start_time = time.time()


external_stylesheets = []

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
server = app.server
app.config.suppress_callback_exceptions = True

connected = False

commandState = CommandState()

try:
    time.sleep(2)
    arduino_helper.update_duty_cycle(0)
    connected = True
except Exception as e:
    print(e)

app.layout = html.Div(
    [
        html.Div(
            id=header_id,
            children=[
                html.H2("Arduino Temperature Controller"),
            ],
            # className="banner",
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                temperature_graph.layout
                            ],
                            className="card graphg",
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        control_panel.layout
                                    ],
                                    className="card controlg",
                                ),
                                html.Div(
                                    [
                                        led_display_panel.layout
                                    ],
                                    className="card ledg",
                                ),
                            ],
                            # className="row",
                        ),
                        html.Div([
                            html.Div(
                                [
                                    settings_panel.layout
                                ],
                                className="card settingsg",
                            ),
                        ],
                            # className="row",
                        ),
                        html.Div(
                            [
                                html.Div(id=stop_time_id),
                                html.Div(id=start_time_id),
                                html.Div(id=reset_time_id),
                                html.Div(id=temperature_store_id),
                                html.Div(id=command_string),
                                html.Div(id=export_data_id),
                                dcc.Interval(
                                    id=graph_interval_id, interval=100000, n_intervals=0
                                ),
                            ],
                            style={"visibility": "hidden"},
                        ), ]
                ),
            ],

            className="wrapper")
    ]
)

@app.callback(
    Output(start_time_id, "children"),
    [Input(start_button_id, "n_clicks")]
)
def start_time(clicks):
    if clicks > 0:
        return time.time()
    return 0


@app.callback(
    Output(stop_button_id, "disabled"),
    [Input(start_button_id, "n_clicks")]
)
def start(clicks):
    commandState.Start()
    return False


@app.callback(
    Output(reset_button_id, "disabled"),
    [Input(stop_button_id, "n_clicks")]
)
def stop(clicks):
    commandState.Stop()
    return False


@app.callback(
    Output(start_button_id, "disabled"),
    [Input(reset_button_id, "n_clicks")]
)
def reset(clicks):
    commandState.Reset()
    return False


@app.callback(
    Output(export_button_id, "disabled"),
    [Input(export_button_id, "n_clicks")],
    [State(graph_data_id, "figure")]
)
def export(clicks, figure):
    data = [figure["data"][0]["x"], figure["data"][0]["y"], figure["data"][1]["y"],
            figure["data"][2]["y"], figure["data"][3]["y"], figure["data"][4]["y"]]
    df = pd.DataFrame(data).T
    df.columns = ['time', 'temp', 'dc', 'dev', 'pro', 'int']
    file_name = 'pid_control_data_' + \
        datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.csv'
    df.to_csv(os.path.join('data', file_name))
    return False

# Rate


@app.callback(
    Output(graph_interval_id, "interval"),
    [Input(start_button_id, "n_clicks"),
     Input(refresh_rate_id, "value")],
)
def graph_control(command, rate):
    if commandState.current_command == "START":
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
        return 40
    return 50


@app.callback(
    Output(temperature_store_id, "children"),
    [Input(start_button_id, "n_clicks"),
     Input(graph_interval_id, "n_intervals")],
)
def get_new_temperature(start, rate):
    return arduino_helper.get_temperature()


@app.callback(
    Output(temperature_display_id, "value"),
    [Input(graph_interval_id, "n_intervals")],
    [State(temperature_store_id, "children")],
)
def get_temperature_for_display(interval, temperature):
    if commandState.current_command == "START":
        temperature = "%.2f" % temperature
        return temperature
    else:
        arduino_helper.update_duty_cycle(0)
        return "25.00"


@app.callback(
    Output(duty_cycle_id, "value"),
    [Input(graph_data_id, "figure")],
    [State(duty_cycle_id, "value"),
     State(command_string, "children"),
     State(setpoint_id, "value"),
     State(derivative_time_id, "value"),
     State(conroller_gain_id, "value"),
     State(integral_time_id, "value"),
     State(refresh_rate_id, "value")]
)
def get_new_dc(figure, current_DC, command, PID_setpoint, dev_gain, pro_gain, int_gain, rate):
    if commandState.current_command == "START":
        try:
            delta_time = float(figure["data"][0]["x"]
                               [-1]) - float(figure["data"][0]["x"][-2])
            current_temperature = float(figure["data"][0]["y"][-1])
            previous_temperature = float(figure["data"][0]["y"][-2])
            previous_temperature2 = float(figure["data"][0]["y"][-3])
        except:
            arduino_helper.update_duty_cycle(0)
            return "0.00"

        PID_setpoint = float(PID_setpoint)
        int_gain = float(int_gain)
        pro_gain = float(pro_gain)
        current_DC = float(current_DC)
        dev_gain = float(dev_gain)

        EN_current = PID_setpoint - current_temperature
        EN_previous = PID_setpoint - previous_temperature

        if delta_time > 0 and int_gain > 0:
            change_in_DC = pro_gain * (EN_current - EN_previous + (delta_time/int_gain) * EN_current - dev_gain / delta_time *
                                       (current_temperature - 2 * previous_temperature + previous_temperature2))
            current_DC += change_in_DC

        if current_DC > 1:
            current_DC = 1
        if current_DC < 0:
            current_DC = 0
        arduino_helper.update_duty_cycle(current_DC)
        return "%.2f" % current_DC

    arduino_helper.update_duty_cycle(0)
    return "0.00"


@app.callback(
    Output(graph_data_id, "figure"),
    [Input(temperature_store_id, "children")],
    [State(graph_data_id, "figure"),
     State(command_string, "children"),
     State(start_time_id, "children"),
     State(setpoint_id, "value"),
     State(derivative_time_id, "value"),
     State(conroller_gain_id, "value"),
     State(integral_time_id, "value")],
)
def graph_data(temperature, figure, command, start, PID, dev_gain, pro_gain, int_gain):
    if commandState.current_command == "START":
        times = figure["data"][0]["x"]
        temperatures = figure["data"][0]["y"]
        set_points = figure["data"][1]["y"]
        dev_gains = figure["data"][2]["y"]
        pro_gains = figure["data"][3]["y"]
        int_gains = figure["data"][4]["y"]

        if start == 0:
            times.append(0)
        else:
            times.append(time.time() - float(start))
        temperatures.append(temperature)
        set_points.append(PID)
        dev_gains.append(dev_gain)
        pro_gains.append(pro_gain)
        int_gains.append(int_gain)
    elif commandState.current_command == "RESET":
        times = []
        temperatures = []
        set_points = []
        dev_gains = []
        pro_gains = []
        int_gains = []
        time_now = 0
    else:
        times = figure["data"][0]["x"]
        temperatures = figure["data"][0]["y"]
        set_points = figure["data"][1]["y"]
        dev_gains = figure["data"][2]["y"]
        pro_gains = figure["data"][3]["y"]
        int_gains = figure["data"][4]["y"]
    return {
        "data": [
            go.Scatter(
                x=times,
                y=temperatures,
                mode="markers",
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
                y=dev_gains,
                mode="lines",
                marker={"size": 6},
                name="dev",
                visible=False,
            ),
            go.Scatter(
                x=times,
                y=pro_gains,
                mode="lines",
                marker={"size": 6},
                name="pro",
                visible=False,
            ),
            go.Scatter(
                x=times,
                y=int_gains,
                mode="lines",
                marker={"size": 6},
                name="int",
                visible=False,
            )
        ],
        "layout": go.Layout(
            autosize=True,
            showlegend=True,
            xaxis={"title": "Time (s)", "autorange": True},
            yaxis={"title": "Temperature (°C)", "autorange": True},
            margin={"l": 70, "b": 100, "t": 0, "r": 25},
        ),
    }


if __name__ == '__main__':
    # import pip
    # pip.main(['install', '-r', 'requirements.txt'])

    port = 8050
    url = "http://127.0.0.1:{0}".format(port)
    threading.Timer(2, lambda: webbrowser.open(url)).start()

    app.run_server(debug=False)
