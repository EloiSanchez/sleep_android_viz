from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
from threading import Timer
import os
import webbrowser

import sys

# TODO: This is super weird for me. Is there a better solution?
# Let me know at eloisanchez16@gmail.com
sys.path.append(".")
sys.path.append("./plots")

from plots import sleep_schedule, sleep_duration


def temp_translator(value):
    if value == "Monthly":
        return {"time_granularity": "Month", "time_group": False}
    elif value == "Aggregated Months":
        return {"time_granularity": "Month", "time_group": True}
    else:
        return {"time_granularity": "Year", "time_group": False}


app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE, dbc.icons.BOOTSTRAP])

app.layout = html.Div(
    [
        # Header
        html.Div(
            [
                html.H1(children="You owe me a beer", style={"textAlign": "center"}),
                html.Div(
                    [
                        "This is an interactive AF summary of my sleep",
                        dcc.RadioItems(
                            options=["Monthly", "Aggregated Months", "Yearly"],
                            value="Monthly",
                            id="agg-value",
                        ),
                    ],
                    style={"textAlign": "center"},
                ),
            ]
        ),
        # Body
        html.Div(
            [
                # Column left
                html.Div(
                    [
                        html.H4("Sleep Schedule", style={"textAlign": "left"}),
                        dcc.Graph(figure={}, id="schedule-graph"),
                    ],
                    style={"width": "40%", "min-width": 600},
                ),
                # Column Right
                html.Div(
                    [
                        html.H4("Sleep Duration", style={"textAlign": "left"}),
                        dcc.Graph(figure={}, id="duration-graph"),
                    ],
                    style={"width": "40%", "min-width": 600},
                ),
            ],
            style={
                "display": "flex",
                "flex-flow": "row",
                "justify-content": "space-evenly",
            },
        ),
    ],
)


@callback(
    Output(component_id="schedule-graph", component_property="figure"),
    Input(component_id="agg-value", component_property="value"),
)
def update_schedule(value):
    return sleep_schedule.make_plot(**temp_translator(value), dashboard=True)


@callback(
    Output(component_id="duration-graph", component_property="figure"),
    Input(component_id="agg-value", component_property="value"),
)
def update_duration(value):
    return sleep_duration.make_plot(**temp_translator(value), dashboard=True)


def open_browser():
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        webbrowser.open_new("http://127.0.0.1:1222/")


if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run_server(debug=True, port=1222)
