from dash import html, dcc
import sys

# TODO: This is super weird for me. Is there a better solution?
# Let me know at eloisanchez16@gmail.com
sys.path.append(".")
sys.path.append("./plots")

from plots.utils import DASH_STYLE


def content():
    SIDEBAR_STYLE = {
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": "16rem",
        "padding": "2rem 1rem",
        "background-color": DASH_STYLE["active_color"],
    }

    sidebar = html.Div(
        [
            html.H3("About", className="display-5"),
            html.Hr(),
            dcc.Markdown(
                "This dashboard was created as an end product for a learning project on [**dbt Core**](https://www.getdbt.com/). The project was made while working at [**Nimbus Intelligence**](https://nimbusintelligence.com/) as an Analytics Engineer.",
                style={"font-size": 18},
            ),
            dcc.Markdown(
                "The data comes from the [**Sleep as Android**](https://sleep.urbandroid.org/) app and includes around 4 years of my sleep data. After an initial parsing of the csv file, the data is stored in a local [**SQLite**](https://www.sqlite.org/index.html) database and transformed using **dbt Core**, from raw tables to end tables.",
                style={"font-size": 18},
            ),
            dcc.Markdown(
                "The end tables are queried using [**Pandas**](https://pandas.pydata.org/) and the graphs and dashboard were built using [**Plotly**](https://plotly.com/) and [**Dash**](https://dash.plotly.com/).",
                style={"font-size": 18},
            ),
            html.Hr(),
            html.Div(
                [
                    _get_icon(
                        "bi bi-github",
                        "https://github.com/EloiSanchez/sleep_android_viz",
                    ),
                    _get_icon(
                        "bi bi-linkedin",
                        "https://www.linkedin.com/in/eloi-sanchez-69094a21b/",
                    ),
                    _get_icon("bi bi-briefcase", "https://nimbusintelligence.com/"),
                ],
                style={"display": "flex", "justify-content": "space-around"},
            ),
        ],
        #
        style=SIDEBAR_STYLE,
    )

    return sidebar


def _get_icon(name, url):
    return html.A(
        html.I(className=name, style={"color": "white", "font-size": "40px"}),
        href=url,
    )
