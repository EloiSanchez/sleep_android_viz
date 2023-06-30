from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
from threading import Timer
import os
import webbrowser


import sidebar
import summary


app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.SUPERHERO, dbc.icons.FONT_AWESOME],
    suppress_callback_exceptions=True,
)


sidebar = sidebar.content()

content = html.Div(summary.content(), id="page-content", style={"margin-left": "18rem"})

app.layout = html.Div([sidebar, content])


@callback(Output("page-content", "children"), Input("url", "pathname"))
def page_content(pathname):
    if pathname == "/":
        return html.H1("This will be the summary page")
    elif pathname == "/summary":
        return summary.content()
    elif pathname == "/individual":
        return html.H1("This will be the individual sleep analysis")


def open_browser():
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        webbrowser.open_new("http://127.0.0.1:1222/")


if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run_server(debug=True, port=1222)
