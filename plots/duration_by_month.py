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


def make_plot(testing: bool = False) -> Figure:
    # get data
    df = get_data("fnl_sleep__obt", ("month", "corrected_hours"), testing)

    # group and clean data
    df = df.groupby(by=["month"]).mean().reset_index()
    df["Season"] = get_season(df["month"])
    avg = df["corrected_hours"].mean()

    # make plot
    fig = px.bar(
        df,
        x="month",
        y=["corrected_hours"],
        color="Season",
        title="Sleep duration by month",
        labels={  # replaces default labels by column name
            "value": "Duration in hours",
            "month": "Month",
        },
        color_discrete_map=SEASON_COLORS,
    )

    add_hline(fig, avg)
    default_style(fig)

    save_plot(fig, "duration_by_month", testing)

    return fig


def main():
    fig = make_plot()

    fig.show()


if __name__ == "__main__":
    main()
