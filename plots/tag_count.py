from utils import (
    get_data,
    save_plot,
    default_style,
)
from plotly import express as px
from plotly.graph_objects import Figure


def make_plot(
    time_granularity: str = "Month", time_group: bool = False, testing: bool = False
) -> Figure:
    # get data
    df = get_data("fnl_tag__count", testing=testing).rename(
        columns={"tag": "Tag", "count": "Count", "month": "Month", "year": "Year"},
    )

    if time_granularity == "Month" and time_group is False:
        label = "Date"
        df["Date"] = df["Year"] + "-" + df["Month"]
    else:
        if time_granularity == "Year":
            group_cols = label = "Year"
        else:
            group_cols = label = "Month"
        df = df.groupby([group_cols] + ["Tag"]).sum().reset_index()

    fig = px.bar(df, x=label, y="Count", color="Tag")

    default_style(fig)

    save_plot(fig, "tags", testing)

    return fig


def main():
    fig = make_plot()

    fig.show()


if __name__ == "__main__":
    main()
