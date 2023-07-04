from dash import html, dcc, callback, Output, Input

import sys

# TODO: This is super weird for me. Is there a better solution?
# Let me know at eloisanchez16@gmail.com
sys.path.append(".")
sys.path.append("./plots")

from plots import sleep_schedule, weekly_info, scatter_plot


GRAPH_STYLE = {"height": "35vh", "margin-bottom": "3vh", "max-height": "40vh"}

MARGINS = "0px 50px 50px 50px"

TOP_COLUMN_STYLE = {"width": "70%", "min-width": 400, "margin": MARGINS}

BOT_COLUMN_STYLE = {"width": "50%", "min-widht": 400, "margin": MARGINS}

ROW_STYLE = {"display": "flex", "justify-content": "space-evenly"}

SUMMARY_STYLE = {"font-size": 20}

SCATTER_COLUMNS = [
    "Bed time",
    "Wake up time",
    "Alarm time",
    "Real sleep hours",
    "Noise",
    "Rating",
    "Snoring",
    "Deep Sleep (%)",
    "Cycles",
]


def content():
    dashboard = html.Div(
        [
            # Top row
            html.Div(
                [
                    html.Div(
                        [
                            html.H1(children="Sleep Summary"),
                            html.Hr(),
                            html.Div(
                                [
                                    html.P(
                                        "This page shows a summary of the data from all the sleeps that have been recorded and uploaded to the app.",
                                        style=dict(
                                            {"margin-top": "30px"}, **SUMMARY_STYLE
                                        ),
                                    ),
                                    html.P(
                                        "There are three graphs displayed. The graph on the right shows the average bed time and wake up time. On the bottom a daily aggregated summary of several variables is displayed, as well as a scatter plot in order to look for possible correlations.",
                                        style=SUMMARY_STYLE,
                                    ),
                                ],
                                style={
                                    "height": "70%",
                                    "display": "flex",
                                    "flex-direction": "column",
                                    "justify-content": "flex-start",
                                    "margin-bottom": "10px",
                                },
                            ),
                        ],
                        style={"width": "30%"},
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H3("Schedule"),
                                    html.Div(
                                        [
                                            html.H5("Grouping:"),
                                            dcc.Dropdown(
                                                options=[
                                                    _get_dropdown_element("Month"),
                                                    _get_dropdown_element(
                                                        "Aggregated months"
                                                    ),
                                                    _get_dropdown_element("Year"),
                                                ],
                                                value="Month",
                                                clearable=False,
                                                id="agg-value",
                                                style={
                                                    "width": "50%",
                                                    "margin-left": "10px",
                                                },
                                            ),
                                            html.H5(
                                                "Coloring:",
                                                style={"margin-left": "0px"},
                                            ),
                                            dcc.Dropdown(
                                                options=[
                                                    {
                                                        "label": html.Span(
                                                            ["Sleep Duration"],
                                                            style={"color": "white"},
                                                        ),
                                                        "value": "Sleep Duration",
                                                    },
                                                    {
                                                        "label": html.Span(
                                                            ["Season"],
                                                            style={"color": "white"},
                                                        ),
                                                        "value": "Season",
                                                    },
                                                ],
                                                value="Sleep Duration",
                                                clearable=False,
                                                id="color-value",
                                                style={
                                                    "width": "50%",
                                                    "margin-left": "10px",
                                                },
                                            ),
                                        ],
                                        style={
                                            "display": "flex",
                                            "justify-content": "start",
                                        },
                                    ),
                                ],
                            ),
                            dcc.Graph(
                                figure={},
                                id="schedule-graph",
                                style=dict(**{"margin-top": "20px"}, **GRAPH_STYLE),
                            ),
                        ],
                        style=TOP_COLUMN_STYLE,
                    ),
                ],
                style=dict({"margin-top": "20px"}, **ROW_STYLE),
            ),
            # Column Right
            html.Div(
                [
                    html.Div(
                        [
                            html.H3("Weekly summary"),
                            dcc.Graph(
                                figure=weekly_info.make_plot(dashboard=True),
                                style=GRAPH_STYLE,
                            ),
                        ],
                        style=BOT_COLUMN_STYLE,
                    ),
                    html.Div(
                        [
                            html.H3("Correlation plot"),
                            dcc.Graph(figure={}, id="scatter-graph", style=GRAPH_STYLE),
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.H5("X axis"),
                                            dcc.Dropdown(
                                                list(
                                                    map(
                                                        _get_dropdown_element,
                                                        SCATTER_COLUMNS,
                                                    )
                                                ),
                                                value="Bed time",
                                                clearable=False,
                                                id="x-value",
                                            ),
                                        ],
                                        style={"width": "30%"},
                                    ),
                                    html.Div(
                                        [
                                            html.H5("Y axis"),
                                            dcc.Dropdown(
                                                list(
                                                    map(
                                                        _get_dropdown_element,
                                                        SCATTER_COLUMNS,
                                                    )
                                                ),
                                                value="Wake up time",
                                                clearable=False,
                                                id="y-value",
                                            ),
                                        ],
                                        style={"width": "30%"},
                                    ),
                                    html.Div(
                                        [
                                            html.H5("Color axis"),
                                            dcc.Dropdown(
                                                list(
                                                    map(
                                                        _get_dropdown_element,
                                                        SCATTER_COLUMNS,
                                                    )
                                                ),
                                                value="Snoring",
                                                clearable=True,
                                                id="scatter-value",
                                            ),
                                        ],
                                        style={"width": "30%"},
                                    ),
                                ],
                                style={
                                    "display": "flex",
                                    "justify-content": "space-evenly",
                                },
                            ),
                        ],
                        style=BOT_COLUMN_STYLE,
                    ),
                ],
                style=ROW_STYLE,
            ),
        ],
    )

    return dashboard


@callback(
    Output(component_id="schedule-graph", component_property="figure"),
    Input(component_id="agg-value", component_property="value"),
    Input(component_id="color-value", component_property="value"),
)
def _update_schedule(agg_value, color_value):
    return sleep_schedule.make_plot(
        **_get_schedule_keys(agg_value), color_by=color_value, dashboard=True
    )


@callback(
    Output(component_id="scatter-graph", component_property="figure"),
    Input(component_id="x-value", component_property="value"),
    Input(component_id="y-value", component_property="value"),
    Input(component_id="scatter-value", component_property="value"),
)
def _update_scatter(x_value, y_value, scatter_value):
    return scatter_plot.make_plot(
        x=x_value, y=y_value, color=scatter_value, size=scatter_value, dashboard=True
    )


def _update_weekly():
    return weekly_info.make_plot(dashboard=True)


def _get_schedule_keys(value):
    if value == "Month":
        return {"time_granularity": "Month", "time_group": False}
    elif value == "Aggregated months":
        return {"time_granularity": "Month", "time_group": True}
    else:
        return {"time_granularity": "Year", "time_group": False}


def _get_dropdown_element(text):
    return {
        "label": html.Span(
            [text],
            style={"color": "white"},
        ),
        "value": text,
    }
