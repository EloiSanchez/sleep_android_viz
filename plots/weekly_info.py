from utils import (
    get_data,
    save_plot,
    default_style,
)
from plotly import express as px
from plotly.graph_objects import Figure


def make_plot(
    active: list = [
        "Bed time",
        "Wake up time",
        "Alarm time",
        "Time in bed",
        "Real sleep hours",
    ],
    dashboard: bool = False,
    testing: bool = False,
) -> Figure:
    column_names = {
        "long_name": "Day",
        "sleep_from": "Bed time",
        "sleep_to": "Wake up time",
        "hours": "Time in bed",
        "corrected_hours": "Real sleep hours",
        "alarm": "Alarm time",
        "snooze": "Snooze",
        "snore": "Snoring",
        "deepsleep": "Deep Sleep (%)",
        "cycles": "Cycles",
    }
    traces = list(column_names.values())

    # get data
    df = get_data(
        "fnl_sleep__weekly",
        (
            "long_name",
            "sleep_from",
            "sleep_to",
            "alarm",
            "snooze",
            "snore",
            "deepsleep",
            "cycles",
            "hours",
            "corrected_hours",
        ),
        testing,
    ).rename(columns=column_names)

    fig = px.bar(
        df,
        x="Day",
        y=traces,
        barmode="group",
        category_orders={
            "Day": [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
            ]
        },
    )

    default_style(fig, dashboard)

    for trace in set(traces).difference(set(active)):
        fig.update_traces(selector={"name": trace}, visible="legendonly")

    if dashboard is False:
        save_plot(fig, "weekly_info", testing)

    return fig


def main():
    fig = make_plot()

    fig.show()


if __name__ == "__main__":
    main()
