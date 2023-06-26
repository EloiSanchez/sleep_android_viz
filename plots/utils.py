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


def default_style(fig: Figure) -> Figure:
    fig.update_layout(width=900, height=600, template="simple_white")
    fig.update_xaxes(showgrid=True)
    fig.update_yaxes(showgrid=True)

    return fig


def add_hline(fig: Figure, y: float) -> None:
    fig.add_hline(y, opacity=1, line_width=1.5, line_dash="dash", line_color="gray")


def save_plot(fig: Figure, name: str, testing: bool = False) -> None:
    if testing is False:
        fig.write_image(
            os.path.join(FILE_DIR, f"figures/png/{name}.png"),
        )
        fig.write_html(
            os.path.join(FILE_DIR, f"figures/html/{name}.html"), full_html=True
        )
