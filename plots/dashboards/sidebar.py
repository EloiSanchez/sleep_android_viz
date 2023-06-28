from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc


def content():
    SIDEBAR_STYLE = {
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": "16rem",
        "padding": "2rem 1rem",
        "background-color": "#353849",
    }

    NAVLINK_STYLE = {"border-radius": "5px", "active": "#3e4452"}

    sidebar = html.Div(
        [
            html.H2("Sidebar", className="display-5"),
            html.Hr(),
            html.P("A simple sidebar layout with navigation links"),
            dbc.Nav(
                [
                    dbc.NavLink("Home", href="/", active="exact", style=NAVLINK_STYLE),
                    dbc.NavLink(
                        "Summary", href="/summary", active="exact", style=NAVLINK_STYLE
                    ),
                    dbc.NavLink(
                        "Individual",
                        href="/individual",
                        active="exact",
                        style=NAVLINK_STYLE,
                    ),
                ],
                vertical=True,
                pills=True,
            ),
        ],
        style=SIDEBAR_STYLE,
    )

    return sidebar
