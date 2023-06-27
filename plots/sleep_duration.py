from utils import (
    get_data,
    get_season,
    save_plot,
    default_style,
    add_hline,
    SEASON_COLORS,
)
from plotly import express as px
from plotly.graph_objects import Figure

from functools import reduce


def make_plot(
    time_granularity: str = "Month",
    time_group: bool = False,
    dashboard: bool = False,
    testing: bool = False,
) -> Figure:
    # get data
    df = get_data(
        "fnl_sleep__obt", ("year", "month", "corrected_hours"), testing
    ).rename(
        columns={"corrected_hours": "Duration", "month": "Month", "year": "Year"},
    )

    # get colums to group with
    if time_granularity == "Month":
        if time_group is False:
            group_cols = ["Year", "Month"]
            label = "Date"
        else:
            group_cols = label = "Month"
    else:
        group_cols = label = "Year"

    # group and clean data
    df = df.groupby(group_cols).mean().reset_index()
    if label == "Date":
        df[label] = reduce(lambda a, b: df[a] + "-" + df[b], group_cols)
    if time_granularity == "Month":
        df["Season"] = get_season(df["Month"])
    avg = df["Duration"].mean()

    # make plot
    fig = px.bar(
        df,
        x=label,
        y="Duration",
        color="Season" if time_granularity == "Month" else "Duration",
        color_continuous_scale=px.colors.sequential.Aggrnyl_r,
        color_discrete_map=SEASON_COLORS,
    )

    add_hline(fig, avg, dashboard)
    default_style(fig, dashboard)

    save_plot(fig, f"duration_by_{label.lower()}", testing)

    return fig


def main():
    fig = make_plot()

    fig.show()


if __name__ == "__main__":
    main()
