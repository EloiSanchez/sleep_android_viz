from utils import (
    get_data,
    default_style,
    save_plot,
    COLUMN_NAMES,
    DASH_STYLE,
    DASH_REF_LINE_STYLE,
)
from plotly import express as px
from plotly.graph_objects import Figure


def make_plot(
    x: str = "Bed time",
    y: str = "Wake up time",
    color: str = "Snoring",
    size: str = "Snoring",
    dashboard: bool = False,
    testing: bool = False,
) -> Figure:
    # get data
    df = get_data(
        "fnl_sleep__obt",
        (
            "sleep_from",
            "sleep_to",
            "sched",
            "corrected_hours",
            "noise",
            "snore",
            "rating",
            "cycles",
            "deepsleep",
        ),
        testing,
    ).rename(columns=COLUMN_NAMES)

    for col in set((x, y, color, size)):
        df = df[df[col] >= 0] if col not in ("Bed time", "Wake up time") else df

    df[size] = df[size].where(df[size] >= 1, 1)
    df = df[df["Real sleep hours"] > 2]

    fig = px.scatter(
        df,
        x=x,
        y=y,
        size=size,
        color=color,
        trendline="ols",
        trendline_color_override=DASH_REF_LINE_STYLE["line_color"],
        marginal_y="violin",
        marginal_x="violin",
        color_continuous_scale=px.colors.sequential.Aggrnyl_r,
    )
    default_style(fig, dashboard)

    fig.update_layout(
        xaxis_title=x,
        yaxis_title=y,
    )
    # fig.update_traces(marker_line_color=DASH_STYLE["ref_line_color"])

    fig.update_traces(
        marker_color=DASH_STYLE["text_color"],
        opacity=0.8,
        selector=dict(type="violin"),
    )

    fig.update_traces(
        line_dash=DASH_REF_LINE_STYLE["line_dash"],
        line_width=DASH_REF_LINE_STYLE["line_width"],
        selector=dict(mode="lines"),
    )

    # Manually change the size of the margins
    fig["layout"]["xaxis"]["domain"] = [0, 0.9]
    fig["layout"]["xaxis3"]["domain"] = [0, 0.9]
    fig["layout"]["xaxis2"]["domain"] = [0.9, 1]
    fig["layout"]["xaxis4"]["domain"] = [0.9, 1]

    fig["layout"]["yaxis"]["domain"] = [0, 0.9]
    fig["layout"]["yaxis2"]["domain"] = [0, 0.9]
    fig["layout"]["yaxis3"]["domain"] = [0.9, 1]
    fig["layout"]["yaxis4"]["domain"] = [0.9, 1]

    return fig


def main():
    fig = make_plot(dashboard=True)

    fig.show()


if __name__ == "__main__":
    main()
