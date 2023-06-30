from dash import html, dcc, callback, Output, Input

import sys

# TODO: This is super weird for me. Is there a better solution?
# Let me know at eloisanchez16@gmail.com
sys.path.append(".")
sys.path.append("./plots")

from plots import sleep_schedule, sleep_duration, tag_count, weekly_info, scatter_plot


GRAPH_STYLE = {"height": "35vh", "margin-bottom": "3vh"}


COLUMN_STYLE = {
    "width": "40%",
    "min-width": 400,
}


def content():
    header = html.Div(
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
    )

    dashboard = html.Div(
        [
            # Column left
            html.Div(
                [
                    html.H4("Sleep Schedule", style={"textAlign": "left"}),
                    dcc.Graph(figure={}, id="schedule-graph", style=GRAPH_STYLE),
                    # html.Hr(),
                    html.H4("Weekly summary"),
                    dcc.Graph(
                        figure=weekly_info.make_plot(dashboard=True), style=GRAPH_STYLE
                    ),
                ],
                style=COLUMN_STYLE,
            ),
            # # Column Center
            # html.Div(
            #     [
            #         html.H4("Sleep Duration", style={"textAlign": "left"}),
            #         dcc.Graph(figure={}, id="duration-graph", style=GRAPH_STYLE),
            #     ],
            #     style=COLUMN_STYLE,
            # ),
            # Column Right
            html.Div(
                [
                    html.H4("Sleep Duration", style={"textAlign": "left"}),
                    dcc.Graph(figure={}, id="duration-graph", style=GRAPH_STYLE),
                    html.H4("Tags"),
                    dcc.Graph(figure={}, id="tags-graph", style=GRAPH_STYLE),
                ],
                style=COLUMN_STYLE,
            ),
        ],
        style={
            "display": "flex",
            "flex-flow": "row",
            "justify-content": "space-evenly",
        },
    )

    content = html.Div(
        [
            header,
            dashboard,
        ]
    )

    return content


@callback(
    Output(component_id="schedule-graph", component_property="figure"),
    Input(component_id="agg-value", component_property="value"),
)
def _update_schedule(value):
    return sleep_schedule.make_plot(**_temp_translator(value), dashboard=True)


@callback(
    Output(component_id="duration-graph", component_property="figure"),
    Input(component_id="agg-value", component_property="value"),
)
def _update_duration(value):
    return sleep_duration.make_plot(**_temp_translator(value), dashboard=True)


@callback(
    Output(component_id="tags-graph", component_property="figure"),
    Input(component_id="agg-value", component_property="value"),
)
def _update_tags(value):
    return scatter_plot.make_plot(dashboard=True)


def _update_weekly():
    return weekly_info.make_plot(dashboard=True)


def _temp_translator(value):
    if value == "Monthly":
        return {"time_granularity": "Month", "time_group": False}
    elif value == "Aggregated Months":
        return {"time_granularity": "Month", "time_group": True}
    else:
        return {"time_granularity": "Year", "time_group": False}
