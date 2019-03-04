import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash
import dash_daq as daq

from app import app
from pages import home, main_graph, setup

app.layout = html.Div(children = [
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/pages/home':
         return home.layout
    elif pathname == '/pages/graph':
         return main_graph.layout
    else:
        return home.layout
        # return '404'

if __name__ == '__main__':
    app.run_server(debug=False)