from utils import (
    get_data,
    save_plot,
    default_style,
    add_hline,
)
from plotly import express as px
from plotly.graph_objects import Figure


def make_plot(
    stat: str = "corrected_hours",
    period: str = "day",
    dashboard: bool = False,
    testing: bool = False,
) -> Figure:
    # get data
    df = get_data(
        "fnl_sleep__obt",
        ("sleep_year", "sleep_month", "sleep_week", "sleep_day_of_month", stat),
        testing,
    ).rename(
        columns={
            "sleep_year": "year",
            "sleep_month": "month",
            "sleep_week": "week",
            "sleep_day_of_month": "day_of_month",
        }
    )

    # group and clean data
    if period in ("month", "week"):
        df["period"] = df["year"] + "-" + df[period]
    elif period == "year":
        df["period"] = df["year"]
    elif period == "day":
        df["period"] = df["year"] + "-" + df["month"] + "-" + df["day_of_month"]

    df = df[["period", stat]].groupby(by=["period"]).mean().reset_index()
    avg = df[stat].mean()

    # make plot
    fig = px.line(
        df,
        x="period",
        y=stat,
    )

    add_hline(fig, avg)
    default_style(fig)

    if dashboard is False:
        save_plot(fig, f"{period if period != 'day' else 'dai'}ly_{stat}", testing)

    return fig


def main():
    fig = make_plot()

    fig.show()


if __name__ == "__main__":
    main()
