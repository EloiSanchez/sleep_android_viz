from utils import (
    SEASON_COLORS,
    get_data,
    get_season,
    default_style,
    save_plot,
    add_hline,
)
from plotly import express as px
from plotly.graph_objects import Figure


def make_plot(testing: bool = False) -> Figure:
    # get data
    df = get_data(
        "fnl_sleep__obt", ("year", "month", "sleep_from", "hours", "sched"), testing
    ).rename(columns={"sleep_from": "Bed time", "hours": "Duration"})

    # group and clean data
    df = df.groupby(["year", "month"]).mean().reset_index()
    df["Date"] = df["year"] + "-" + df["month"]
    df["Season"] = get_season(df["month"])
    df["Sleep Duration"] = df["Duration"]

    bed_time = df["Bed time"].mean()
    wake_up_time = (df["Bed time"] + df["Duration"]).mean()

    # In the plot, duration will become wake up time
    df = df.rename(columns={"Duration": "Wake up time"})

    # make plot
    fig = px.bar(
        df,
        x="Date",
        y="Wake up time",
        base="Bed time",
        color="Season",
        color_discrete_map=SEASON_COLORS,
        labels={"Wake up time": "Sleep schedule", "Date": "Month"},
        # TODO: Make `month` appear first and `wake up time` second on hover menu
        hover_data={
            "Date": True,
            "Wake up time": ":.2f",
            "Bed time": ":.2f",
            "Sleep Duration": ":.2f",
            "Season": False,
        },
    )

    default_style(fig)

    # add horizontal average lines and labels
    add_hline(fig, bed_time)
    add_hline(fig, wake_up_time)

    for label, var in {"Bed time": bed_time, "Wake up time": wake_up_time}.items():
        fig.add_annotation(
            x=df["Date"].min(),
            y=var,
            text=f"Average {label.lower()}",
            showarrow=False,
            yshift=12,
            xshift=5,
            bgcolor="#ffffff",
            opacity=0.8,
            font=dict(color="gray"),
            xanchor="left",
        )

    # make yaxis ticks pretty
    fig.update_layout(
        yaxis=dict(
            tickmode="array",
            tickvals=list(range(24)),
            ticktext=[f"{x}:00" for x in range(24)],
        ),
    )

    # show grid
    fig.update_xaxes(showgrid=True)
    fig.update_yaxes(showgrid=True)

    save_plot(fig, "schedule_by_year_month", testing)

    return fig


def main():
    fig = make_plot()

    fig.show()


if __name__ == "__main__":
    main()
