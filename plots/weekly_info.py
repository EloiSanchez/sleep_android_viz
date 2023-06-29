from utils import (
    get_data,
    save_plot,
    default_style,
)
from plotly import express as px
from plotly.graph_objects import Figure


def make_plot(
    to_plot: list = ["Bed time", "Wake up time", "Alarm time"],
    dashboard: bool = False,
    testing: bool = False,
) -> Figure:
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
    ).rename(
        columns={
            "long_name": "Day",
            "sleep_from": "Bed time",
            "sleep_to": "Wake up time",
            "alarm": "Alarm time",
            "snooze": "Snooze",
            "snore": "Snoring",
            "deepsleep": "Deep Sleep (%)",
            "cycles": "Cycles",
            "hours": "Time in bed",
            "corrected_hours": "Real sleep hours",
        }
    )

    fig = px.bar(
        df,
        x="Day",
        y=to_plot,
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

    if dashboard is False:
        save_plot(fig, "weekly_info", testing)

    return fig


def main():
    fig = make_plot()

    fig.show()


if __name__ == "__main__":
    main()
