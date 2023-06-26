from utils import (
    SEASON_COLORS,
    get_data,
    get_season,
    default_style,
    save_plot,
    add_hline,
    to_hour,
)
from plotly import express as px
from plotly.graph_objects import Figure

from functools import reduce


def make_plot(
    time_granularity: str = "Month", time_group: bool = False, testing: bool = False
) -> Figure:
    # get data
    df = get_data(
        "fnl_sleep__obt", ("year", "month", "sleep_from", "hours", "sched"), testing
    ).rename(
        columns={
            "sleep_from": "Bed time",
            "hours": "Duration",
            "month": "Month",
            "year": "Year",
        }
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
    df["Sleep Duration"] = df["Duration"]

    bed_time = df["Bed time"].mean()
    wake_up_time = (df["Bed time"] + df["Duration"]).mean()

    # In the plot, duration will become wake up time
    df = df.rename(columns={"Duration": "Wake up time"})

    # make plot
    fig = px.bar(
        df,
        x=label,
        y="Wake up time",
        base="Bed time",
        color="Sleep Duration",
        color_discrete_map=SEASON_COLORS,
        color_continuous_scale=px.colors.sequential.Aggrnyl_r,
        labels={"Wake up time": "Sleep schedule", "Date": "Month"},
        # TODO: Make `Month` appear first and `wake up time` second on hover menu
        hover_data={
            label: True,
            "Wake up time": ":.2f",
            "Bed time": ":.2f",
            "Sleep Duration": ":.2f",
        },
    )

    default_style(fig)

    # add horizontal average lines and labels
    add_hline(fig, bed_time)
    add_hline(fig, wake_up_time)

    # make yaxis ticks pretty
    ticks = list(range(24)) + [bed_time, wake_up_time]
    fig.update_layout(
        yaxis=dict(
            tickmode="array",
            tickvals=ticks,
            ticktext=[f"{to_hour(x)}" for x in ticks],
        ),
    )

    save_plot(fig, f"schedule_by_{label.lower()}", testing)

    return fig


def main():
    fig = make_plot(time_granularity="Month", time_group=False)

    fig.show()


if __name__ == "__main__":
    main()
