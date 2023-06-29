import pandas as pd
import sqlite3
import os
from plotly.graph_objects import Figure

from typing import Union, Iterable


SEASONS = {
    "01": "Winter",
    "02": "Winter",
    "03": "Winter",
    "04": "Spring",
    "05": "Spring",
    "06": "Spring",
    "07": "Summer",
    "08": "Summer",
    "09": "Summer",
    "10": "Autumn",
    "11": "Autumn",
    "12": "Autumn",
}

SEASON_COLORS = {
    "Winter": "#4BCEDD",
    "Spring": "#6FB668",
    "Summer": "#F2C14E",
    "Autumn": "#F77F50",
}

DASH_STYLE = {"base_color": "#2e3141", "line_color": "#5c6571", "text_color": "#aaaaaa"}

FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)
DB_DIR = os.path.os.path.join(FILE_PATH, "../../database/")


def get_data(
    table_name: str, columns: Union[None, Iterable[str]] = "*", testing: bool = False
) -> pd.DataFrame:
    # Get the database directory independent of the path where the script executes

    con = sqlite3.connect(os.path.join(DB_DIR, "final.db"))

    if columns != "*":
        columns = ", ".join(columns)

    query = f"""select {columns} from {table_name}"""

    if testing:
        query += "\nlimit 100"

    return pd.read_sql(query, con)


def get_season(month: pd.Series) -> pd.Series:
    return pd.Series(map(lambda x: SEASONS[x], month), name="Season")


def default_style(fig: Figure, dashboard: bool = False) -> Figure:
    if dashboard is True:
        fig.update_layout(
            template="simple_white",
            paper_bgcolor=DASH_STYLE["base_color"],
            plot_bgcolor=DASH_STYLE["base_color"],
            font=dict(color=DASH_STYLE["text_color"]),
            margin=dict(b=0, l=0, r=0, t=0),
            xaxis_title=None,
            yaxis_title=None,
        )
        fig.update_xaxes(
            gridcolor=DASH_STYLE["line_color"],
            tickcolor=DASH_STYLE["base_color"],
            linecolor=DASH_STYLE["base_color"],
            showgrid=True,
        )
        fig.update_yaxes(
            gridcolor=DASH_STYLE["line_color"],
            tickcolor=DASH_STYLE["base_color"],
            linecolor=DASH_STYLE["base_color"],
            showgrid=True,
        )
        fig.update_traces(marker_line_color=DASH_STYLE["base_color"])
    else:
        fig.update_layout(width=900, height=500, template="simple_white")
        fig.update_yaxes(showgrid=True)
        fig.update_xaxes(showgrid=True)

    return fig


def to_hour(time: float) -> str:
    hh = round(time)
    mm = int((time - hh) * 60)
    return f"{hh:d}:{mm:0>2d}"


def add_hline(fig: Figure, y: float, dashboard: bool = False) -> None:
    fig.add_hline(
        y,
        opacity=1,
        line_width=1.5,
        line_dash="dash",
        line_color="#D0D4D9" if dashboard is True else "gray",
    )


def save_plot(fig: Figure, name: str, testing: bool = False) -> None:
    if testing is False:
        fig.write_image(
            os.path.join(FILE_DIR, f"figures/png/{name}.png"),
        )
        fig.write_html(
            os.path.join(FILE_DIR, f"figures/html/{name}.html"), full_html=True
        )
