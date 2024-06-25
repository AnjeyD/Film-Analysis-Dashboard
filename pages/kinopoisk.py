import dash
from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
from data import df, all_g, all_year, all_cont, directors

layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H1("Полный подбор фильма"),
                html.Hr(style={'color': 'black'}),
            ], style={'textAlign': 'center'})
        )
    ]),

    html.Br(),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H3('Жанры'),
                dcc.Dropdown(
                    id='crossfilter-genre',
                    options=[{'label': i, 'value': i} for i in all_g],
                    value='',
                    multi=True,
                    clearable=False,
                    style={'width': '100%'}  # Ширина Dropdown
                )
            ]),
            width=3,
        ),

        dbc.Col(
            html.Div([
                html.H3('Год'),
                dcc.Dropdown(
                    id='crossfilter-year',
                    options=[{'label': i, 'value': i} for i in all_year],
                    value='2000',
                    multi=True,
                    clearable=False,
                    style={'width': '100%'}  # Ширина Dropdown
                )
            ]),
            width=3,
        ),

        dbc.Col(
            html.Div([
                html.H3('Страна'),
                dcc.Dropdown(
                    id='crossfilter-country',
                    options=[{'label': i, 'value': i} for i in all_cont],
                    value='USA',
                    multi=True,
                    clearable=False,
                    style={'width': '100%'}  # Ширина Dropdown
                )
            ]),
            width=3,
        ),

        dbc.Col(
            html.Div([
                html.H3('Режиссер'),
                dcc.Dropdown(
                    id='crossfilter-director',
                    options=[{'label': i, 'value': i} for i in directors],
                    value='',
                    multi=True,
                    clearable=False,
                    style={'width': '100%'}  # Ширина Dropdown
                )
            ]),
            width=3,
        )
    ]),

    html.Br(),

    dbc.Row([
        html.Div([
            html.H5("Выберите рейтинг:"),
        ], style={'textAlign': 'left'})

    ]),
    html.Br(),
    html.Div(
        dcc.Slider(
            id='crossfilter-rating',
            min=df['avg_vote'].min(),
            max=df['avg_vote'].max(),
            value=5.0,
            step=None,
            marks=None,
            tooltip={
                "always_visible": True,
                "style": {"color": "LightSteelBlue", "fontSize": "20px"},
                "placement": "bottom",
            }
        ), style={'width': '95%', 'padding': '0px 20px 20px 20px', 'text_color': 'black'}
    ),

    dbc.Row([
        dbc.Col(
            html.Div(id='film-count', style={'fontSize': '20px', 'fontWeight': 'bold'})
        )
    ]),

    dbc.Row(id='film-cards-row'),
    
])

# Callback для обновления карточек фильмов по выбранным фильтрам и отображения количества фильмов
@callback(
    [Output('film-count', 'children'),
     Output('film-cards-row', 'children')],
    [Input('crossfilter-genre', 'value'),
     Input('crossfilter-year', 'value'),
     Input('crossfilter-country', 'value'),
     Input('crossfilter-director', 'value'),
     Input('crossfilter-rating', 'value')]
)
def update_film_cards(selected_genres, selected_years, selected_countries, selected_directors, selected_rating):
    filtered_data = df.copy()

    # Применяем фильтрацию по жанрам
    if selected_genres:
        filtered_data = filtered_data[filtered_data['genre'].isin(selected_genres)]

    # Применяем фильтрацию по годам
    if selected_years:
        if isinstance(selected_years, str):
            selected_years = [selected_years]
        filtered_data = filtered_data[filtered_data['year'].isin(selected_years)]

    # Применяем фильтрацию по странам
    if selected_countries:
        filtered_data = filtered_data[filtered_data['country'].apply(lambda x: isinstance(x, str) and any(country in x.split(', ') for country in selected_countries))]

    # Применяем фильтрацию по режиссерам
    if selected_directors:
        filtered_data = filtered_data[filtered_data['directors'].apply(lambda x: isinstance(x, str) and any(director in x.split(', ') for director in selected_directors))]

    # Применяем фильтрацию по рейтингу
    filtered_data = filtered_data[filtered_data['avg_vote'] >= selected_rating]

    film_count = len(filtered_data)

    # Ограничиваем до 200 фильмов
    filtered_data = filtered_data.head(200)

    # Создаем карточки для отображения
    film_cards = []

    for index, row in filtered_data.iterrows():
        card = dbc.Card(
            [   
                dbc.CardHeader(
                    html.H4(row['title'], className="card-title"),
                    style={'text-align': 'center', 'height': 'fit-content'},                  
                ),
                dbc.CardBody(
                    [
                        html.H4(row['genre'], className="card-subtitle mb-2 text-muted"),                      # Добавляем жанр
                        html.P(f"Год: {row['year']}", style={'fontSize': '1.25rem'}),                                                         # Добавляем год
                        html.P(f"Страна: {row['country']}", style={'fontSize': '1.25rem'}),                                                   # Добавляем страну
                        html.P(f"Режиссеры: {row['directors']}", style={'fontSize': '1.25rem'}),                                              # Добавляем режисера
                        html.P(f"Рейтинг: {row['avg_vote']}", className="card-text text-right text-info", style={'fontSize': '1.25rem'}),     # Добавляем рейтинг
                    ]
                ),
                dbc.CardFooter([
                    dbc.Button("Описание", id=f"description-button-{index}", color="primary", className="mb-3"),
                    dbc.Modal([
                        dbc.ModalHeader([
                            html.P(f"{row['title']}", className="modal-title", style={'fontSize': '1.75rem', 'align-text': 'center'})
                        ]),
                        dbc.ModalBody([
                            html.P(f"Описание: {row['description']}", style={'fontSize': '1.25rem'}),
                            html.P(f"Примечания: {row['notes']}", style={'fontSize': '1.25rem'})
                        ]),
                        dbc.ModalFooter(
                            dbc.Button("Закрыть", id=f"close-button-{index}", className="ml-auto")
                        ),
                    ], id=f"modal-{index}", size="lg")
                ])
            ],
            style={"width": "19rem", "margin": "10px"}
        )
    
        film_cards.append(dbc.Col(card, width=3, className="d-flex align-items-stretch"))


    return f"Найдено фильмов: {film_count}", film_cards

for index, row in df.iterrows():
    @callback(
        Output(f"modal-{index}", "is_open"),
        [Input(f"description-button-{index}", "n_clicks"),
         Input(f"close-button-{index}", "n_clicks")],
        [dash.dependencies.State(f"modal-{index}", "is_open")]
    )
    def toggle_modal(n1, n2, is_open):
        if n1 or n2:
            return not is_open
        return is_open
