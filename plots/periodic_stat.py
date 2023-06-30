from utils import get_data, save_plot, default_style, add_hline, COLUMN_NAMES
from plotly import express as px
from plotly.graph_objects import Figure


def make_plot(
    stat: str = "Real sleep hours",
    period: str = "Day",
    dashboard: bool = False,
    testing: bool = False,
) -> Figure:
    # get data
    df = get_data(
        "fnl_sleep__obt",
        testing=testing,
    ).rename(columns=COLUMN_NAMES)

    # group and clean data
    if period in ("Month", "Week"):
        df["Date"] = df["Year"] + "-" + df[period]
    elif period == "Year":
        df["Date"] = df["Year"]
    elif period == "Day":
        df["Date"] = df["Year"] + "-" + df["Month"] + "-" + df["Day"]

    df = df[["Date", stat]].groupby(by=["Date"]).mean().reset_index()
    avg = df[stat].mean()

    # make plot
    fig = px.line(
        df,
        x="Date",
        y=stat,
    )

    add_hline(fig, avg)
    default_style(fig, dashboard=dashboard)

    if dashboard is False:
        save_plot(fig, f"{period if period != 'day' else 'dai'}ly_{stat}", testing)

    return fig


def main():
    fig = make_plot()

    fig.show()


if __name__ == "__main__":
    main()
