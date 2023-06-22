from utils import get_data, get_season, save_plot, SEASON_COLORS
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
        width=900,
        height=600,
        labels={  # replaces default labels by column name
            "value": "Duration in hours",
            "month": "Month",
        },
        color_discrete_map=SEASON_COLORS,
        template="simple_white",
    )
    fig.add_hline(avg, opacity=1, line_width=1.5, line_dash="dash", line_color="gray")

    # show grid
    fig.update_xaxes(showgrid=True)
    fig.update_yaxes(showgrid=True)

    save_plot(fig, "duration_by_month", testing)

    return fig


def main():
    fig = make_plot()

    fig.show()


if __name__ == "__main__":
    main()
