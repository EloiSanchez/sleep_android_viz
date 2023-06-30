from utils import get_data, save_plot, default_style, COLUMN_NAMES
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
    # get data
    df = get_data(
        "fnl_sleep__weekly",
        (
            "long_name",
            "sleep_from",
            "sleep_to",
            "alarm",
            "hours",
            "corrected_hours",
            "snooze",
            "snore",
            "deepsleep",
            "cycles",
        ),
        testing,
    ).rename(columns=COLUMN_NAMES)

    fig = px.bar(
        df,
        x="Day",
        y=df.columns,
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

    # Deactivate some variables by default
    for trace in set(df.columns).difference(set(active)):
        fig.update_traces(selector={"name": trace}, visible="legendonly")

    if dashboard is False:
        save_plot(fig, "weekly_info", testing)

    return fig


def main():
    fig = make_plot()

    fig.show()


if __name__ == "__main__":
    main()
