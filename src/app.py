# BASE CODE, FALLBACK IF NEEDED
# import dash
# from dash import dcc, html
# import pandas as pd
# import plotly.express as px

# # Sample data
# df = pd.DataFrame({
#     "Category": ["A", "B", "C", "D"],
#     "Values": [23, 45, 12, 67]
# })

# # Create figure
# fig = px.bar(df, x="Category", y="Values", title="Sample Bar Chart")

# # Create Dash app
# app = dash.Dash(__name__)

# app.layout = html.Div(children=[
#     html.
#     html.H1("Big Data Project Visualization"),
#     dcc.Graph(figure=fig)
# ])

# if __name__ == '__main__':
#     app.run_server(debug=True)

from dash import Dash, Input, Output
from dash import html, dcc

import dash_bootstrap_components as dbc

home_layout = html.Div(children=[html.H1(children="This is our Home page")])

data_upload_layout = html.Div(
    children=[html.H1(children="This is our upload page")]
)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Data upload", href="/data_upload")),
    ],
    brand="Multipage Dash App",
    color="dark",
    dark=True,
    className="mb-2",
)

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        navbar,
        dbc.Container(id="page-content", className="mb-4", fluid=True),
    ]
)

# Example code
@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    if pathname == "/":
        return home_layout
    elif pathname == "/data_upload":
        return data_upload_layout
    else:
        return dbc.Jumbotron(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognized..."),
            ]
        )


if __name__ == "__main__":
    app.run()