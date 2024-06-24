from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
from data import df

# Создание layout для Dash
layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H1("Топ-10 фильмов"),
                html.Hr(style={'color': 'black'}),
            ], style={'textAlign': 'center'})
        )
    ]),
    
    html.Br(),

    dbc.Row([
        dbc.Col(
            html.Div([
                html.H3("Выберите год:"),
            ], style={'textAlign': 'left'})
        )
    ]),
    
    html.Br(),
    
    dbc.Row([
        dbc.Col(
            html.Div(
                dcc.RangeSlider(
                    id='crossfilter-year',
                    min=df['year'].min(),
                    max=df['year'].max(),
                    value=[2000, 2005],
                    step=None,
                    marks=None,
                    tooltip={
                        "always_visible": True,
                        "style": {"color": "LightSteelBlue", "fontSize": "20px"},
                        "placement": "bottom",
                    }
                ), style={'width': '95%', 'padding': '0px 20px 20px 20px'}
            )
        )
    ]),

    dbc.Row([
        dbc.Col(
            dcc.Graph(id='genre-count-graph', figure={}),
            width = 6,
        ),
        dbc.Col(
            dcc.Graph(id='director-count-graph', figure={}),
            width = 6,
        )
    ]),

    
    dbc.Row([
        dbc.Col(
            dcc.Graph(id='country-count-graph', figure={}),
            width = 6,
        ),
        dbc.Col(
            dcc.Graph(id='actor-bar-chart', figure={}),
            width = 6,
        )
    ]),

], fluid=True)


def filter_data(selected_years):
    return df[(df['year'] >= selected_years[0]) & (df['year'] <= selected_years[1])]

@callback(
    Output('genre-count-graph', 'figure'),
    Input('crossfilter-year', 'value')
)
def update_genre_graph(selected_years):
    filtered_df = filter_data(selected_years)
    genre_counts = (filtered_df.set_index(['year'])['genre']
                    .str.split(', ', expand=True)
                    .stack()
                    .reset_index(name='genre')
                    .drop(columns='level_1')
                    .dropna()
                    .groupby(['year', 'genre'])
                    .size()
                    .reset_index(name='count')
                    .sort_values(['year', 'count'], ascending=[True, False])
                    .groupby('year')
                    .head(10))
    
    genre_fig = px.bar(genre_counts, x='year', y='count', color='genre',
                       title='ТОП-10 популярных жанров:',
                       labels={'genre': 'Жанр', 'count': 'Количество фильмов', 'year': 'Год'})
    
    return genre_fig

@callback(
    Output('director-count-graph', 'figure'),
    Input('crossfilter-year', 'value')
)
def update_director_graph(selected_years):
    filtered_df = filter_data(selected_years)
    director_counts = (filtered_df.set_index(['year'])['directors']
                       .str.split(', ', expand=True)
                       .stack()
                       .reset_index(name='directors')
                       .drop(columns='level_1')
                       .dropna()
                       .groupby(['year', 'directors'])
                       .size()
                       .reset_index(name='count')
                       .sort_values(['year', 'count'], ascending=[True, False])
                       .groupby('year')
                       .head(10))
    
    director_fig = px.bar(director_counts, x='year', y='count', color='directors',
                          title='ТОП-10 популярных режиссеров:',
                          labels={'directors': 'Режиссер', 'count': 'Количество фильмов', 'year': 'Год'})
    
    return director_fig

@callback(
    Output('country-count-graph', 'figure'),
    Input('crossfilter-year', 'value')
)
def update_country_graph(selected_years):
    filtered_df = filter_data(selected_years)
    country_counts = (filtered_df.set_index(['year'])['country']
                      .str.split(', ', expand=True)
                      .stack()
                      .reset_index(name='country')
                      .drop(columns='level_1')
                      .dropna()
                      .groupby(['year', 'country'])
                      .size()
                      .reset_index(name='count')
                      .sort_values(['year', 'count'], ascending=[True, False])
                      .groupby('year')
                      .head(10))
    
    country_fig = px.bar(country_counts, x='year', y='count', color='country',
                         title='ТОП-10 стран производителей:',
                         labels={'country': 'Страна', 'count': 'Количество фильмов', 'year': 'Год'})
    
    return country_fig

@callback(
    Output('actor-bar-chart', 'figure'),
    Input('crossfilter-year', 'value')
)
def update_actor_bar_chart(selected_years):
    filtered_df = filter_data(selected_years)
    actor_counts = (filtered_df.set_index(['year'])['actors']
                    .str.split(', ', expand=True)
                    .stack()
                    .reset_index(name='actor')
                    .drop(columns='level_1')
                    .dropna()
                    .groupby(['year', 'actor'])
                    .size()
                    .reset_index(name='film_count')
                    .sort_values(['year', 'film_count'], ascending=[True, False])
                    .groupby('year')
                    .head(10))
    
    actor_fig = px.bar(actor_counts, x='year', y='film_count', color='actor',
                       title='ТОП-10 самых популярных актеров:',
                       labels={'actor': 'Актёр', 'film_count': 'Количество фильмов', 'year': 'Год'})
    
    return actor_fig
