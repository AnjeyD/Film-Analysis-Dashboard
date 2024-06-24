import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, dcc, html
from pages import amain, kinopoisk, topfilm, xstatistics


external_stylesheets = [dbc.themes.SKETCHY]  # Вместо FLATLY выберите свою тему из https://bootswatch.com/
app = Dash(__name__, external_stylesheets=external_stylesheets,  use_pages=True)
app.config.suppress_callback_exceptions = True

# Задаем аргументы стиля для боковой панели. Мы используем position:fixed и фиксированную ширину
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#17A2B8", # Цвет фона боковой панели 
}

# Справа от боковой панели размешается основной дашборд. Добавим отступы
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2(
            ["Долженко А.В.", html.Br(), "Седова М.А."],
            className="lead"
        ),
        html.Hr(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.H2("МЕНЮ", className="display-6", style={"text-align": "center"}),
        dbc.Nav(
            [
                dbc.NavLink("Главная", href="/", active="exact"),
                dbc.NavLink("Подбор фильма", href="/kinopoisk", active="exact"),
                dbc.NavLink("Топ-10", href="/topfilm", active="exact"),
                dbc.NavLink("Статистика", href="/xstatistics", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")])

def render_page_content(pathname):
    if pathname == "/":
        return amain.layout
    elif pathname == "/kinopoisk":
        return kinopoisk.layout
    elif pathname == "/topfilm":
        return topfilm.layout
    elif pathname == "/xstatistics":
        return xstatistics.layout
    # Если пользователь попытается перейти на другую страницу, верните сообщение 404.
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )

if __name__ == '__main__':
        app.run_server(debug=True)
