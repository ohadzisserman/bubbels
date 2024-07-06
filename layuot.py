from dash import Dash, html
def create_layout(app: Dash) -> html.Div:
    return html.Div(
        className="my appush",
        children=[
            html.H1(app.title),
            html.Hr()
        ]
    )