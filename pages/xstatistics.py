from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
from data import df, critics_avg_by_genre, public_avg_by_genre, duration_avg_by_genre, film_count_by_genre, all_cont, all_g  
import pandas as pd
import plotly.graph_objs as go

# Преобразуем тип данных столбца duration из int64 в float64
df['duration'] = df['duration'].astype(float)

RADAR_STYLE = {'width': '50%', 'margin': 'auto'}


layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H1("Статистика по фильмам"),
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
                    value=[1897, 1911],
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
        dcc.Graph(id='country-map', figure={}, style={'height': '80vh', 'width': '100%'}  
        )
    ]),
    
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H2("Статистика по жанрам"),
            ],style={'textAlign': 'center'})
        )
    ]),
    
    html.Br(),

    dbc.Row([
        html.H5("Выберите критерий для отображения:"),
    ]),

    html.Br(),

    dbc.Row([
        dcc.Dropdown(
            id='statistic-dropdown',
            options=[
                {'label': 'Средняя оценка критиков и зрителей', 'value': 'both_votes'},
                {'label': 'Средняя продолжительность фильмов', 'value': 'duration'},
                {'label': 'Количество фильмов', 'value': 'film_count'}
            ],
            value='both_votes',
            clearable=False
        )
    ]),

    html.Br(),

    dbc.Row([
        dbc.Col(
            dcc.Graph(id='genre-stats')
        )
    ]),

    html.Br(),

    dbc.Row([
        dbc.Col(
            html.Div([
                html.H2("Диаграмма оценок фильмов от итальянского интернет-сервиса FilmTV"),
            ],style={'textAlign': 'center'})
        )
    ]),

    html.Br(),

    dbc.Row([
        dbc.Col(
            html.Div([
                html.H5('Выберите страну'),
                dcc.Dropdown(
                    id='country-dropdown',
                    options=[{'label': i, 'value': i} for i in all_cont],
                    value='USA',
                    multi=True,
                    clearable=False,
                    style={'width': '100%'}
                )
            ]),
            width=6,
        ),

        dbc.Col(
            html.Div([
                html.H5('Выберите жанр'),
                dcc.Dropdown(
                    id='genre-dropdown',
                    options=[{'label': i, 'value': i} for i in all_g],
                    value='',
                    multi=True,
                    clearable=False,
                    style={'width': '100%'}
                )
            ]),
            width=6,
        ), 
    ]),

    html.Br(),

    dbc.Row([
        dbc.Col(
            html.Div(id='alert-container', style={'text-align': 'center', 'margin-top': '20px'}),
            width=12,
        ),
    ]),
    
    dbc.Row([
        dbc.Col(
            dcc.Graph(id='scatter-plot'),
            width=12
        )
    ]),

    html.Br(),

], fluid=True)

#График-1 КАРТА
@callback(
    Output('country-map', 'figure'),
    Input('crossfilter-year', 'value')
)
def update_country_map(year_range):
    filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
    
    # Создаем DataFrame для хранения данных о странах, количестве фильмов, жанрах, оценках и продолжительности
    country_film_counts = pd.DataFrame(columns=['country', 'film_count'])
    country_genre_counts = pd.DataFrame(columns=['country', 'film_count', 'genre'])
    country_stats = pd.DataFrame(columns=['country', 'critics_vote', 'public_vote', 'duration'])

    # Проходимся по каждой строке и разделяем фильмы с несколькими странами производителями и жанрами
    for index, row in filtered_df.iterrows():
        countries = row['country']
        genres = row['genre']
        if isinstance(countries, str):
            countries = countries.split(', ')
        else:
            continue
        if isinstance(genres, str):
            genres = genres.split(', ')
        else:
            genres = ['Unknown']
        
        for country in countries:
            # Учитываем количество фильмов
            country_film_counts = pd.concat([country_film_counts, pd.DataFrame({'country': [country], 'film_count': [1]})], ignore_index=True)
            # Учитываем жанры
            for genre in genres:
                country_genre_counts = pd.concat([country_genre_counts, pd.DataFrame({'country': [country], 'film_count': [1], 'genre': [genre]})], ignore_index=True)
            # Учитываем оценки и продолжительность (заменяем пропуски на 0)
            critics_vote = row['critics_vote'] 
            public_vote = row['public_vote'] 
            duration_value = row['duration']  # Получаем значение продолжительности для текущей строки
            country_stats = pd.concat([country_stats, pd.DataFrame({'country': [country], 'critics_vote': [critics_vote], 'public_vote': [public_vote], 'duration': [duration_value]})], ignore_index=True)
    
    # Группируем по странам и считаем общее количество фильмов
    country_film_counts = country_film_counts.groupby('country').sum().reset_index()

    # Группируем по странам и жанрам и считаем общее количество фильмов
    country_genre_counts = country_genre_counts.groupby(['country', 'genre']).sum().reset_index()

    # Находим самый популярный жанр для каждой страны
    most_popular_genre = country_genre_counts.loc[country_genre_counts.groupby('country')['film_count'].idxmax()]

    # Группируем по странам и считаем средние оценки и продолжительность (заменяем пропущенные значения на 0)
    country_stats = country_stats.groupby('country').mean(numeric_only=True).reset_index()
    country_stats['critics_vote'] = country_stats['critics_vote'].fillna(0)
    country_stats['public_vote'] = country_stats['public_vote'].fillna(0)
    country_stats['duration'] = country_stats['duration'].fillna(0)

    # Объединяем данные по количеству фильмов, популярным жанрам и статистике
    merged_data = pd.merge(country_film_counts, most_popular_genre[['country', 'genre']], on='country', how='left')
    merged_data = pd.merge(merged_data, country_stats, on='country', how='left')

    # Создаем карту
    fig = px.choropleth(
        merged_data,
        locations='country',
        locationmode='country names',
        color='film_count',
        hover_name='country',
        hover_data={
            'genre': True,
            'critics_vote': ':.2f',
            'public_vote': ':.2f',
            'duration': ':.2f'
        },
        title=f'Количество фильмов, популярные жанры, средняя оценка критиков, зрителей и средняя продолжительность фильмов по странам за {year_range[0]}-{year_range[1]} годы',
        labels={
            'film_count': 'Количество фильмов',
            'country': 'Страна',
            'genre': 'Популярный жанр',
            'critics_vote': 'Средняя оценка критиков',
            'public_vote': 'Средняя оценка зрителей',
            'duration': 'Средняя продолжительность (мин)'
        },
        color_continuous_scale=px.colors.sequential.GnBu
    )
    
    return fig

#График-2
@callback(
    Output('genre-stats', 'figure'),
    Input('statistic-dropdown', 'value')
)
def update_genre_stats(selected_statistic):
    if selected_statistic == 'both_votes':
        fig = go.Figure(data=[
            go.Bar(
                name='Критики',
                x=critics_avg_by_genre.index,
                y=critics_avg_by_genre.values,
                text=critics_avg_by_genre.values,
                textposition='auto',
                marker_color='skyblue',
                hoverinfo='skip'
            ),
            go.Bar(
                name='Зрители',
                x=public_avg_by_genre.index,
                y=public_avg_by_genre.values,
                text=public_avg_by_genre.values,
                textposition='auto',
                marker_color='orange',
                hoverinfo='skip'
            )
        ])
        fig.update_layout(
            title='Средняя оценка критиков и зрителей',
            title_x=0.5,
            xaxis={'title': 'Жанр'},
            yaxis={'title': 'Значение'},
            plot_bgcolor='rgba(0,0,0,0)',
            barmode='group'  # Group bars together
        )
    elif selected_statistic == 'duration':
        data = duration_avg_by_genre
        title = 'Средняя продолжительность фильмов (мин)'
        fig = go.Figure(data=[
            go.Bar(
                x=data.index,
                y=data.values,
                text=data.values,
                textposition='auto',
                marker_color='skyblue'
            )
        ])
        fig.update_layout(
            title=title,
            title_x=0.5,
            xaxis={'title': 'Жанр'},
            yaxis={'title': 'Значение'},
            plot_bgcolor='rgba(0,0,0,0)'
        )
    elif selected_statistic == 'film_count':
        data = film_count_by_genre
        title = 'Количество фильмов'
        fig = go.Figure(data=[
            go.Bar(
                x=data.index,
                y=data.values,
                text=data.values,
                textposition='auto',
                marker_color='skyblue'
            )
        ])
        fig.update_layout(
            title=title,
            title_x=0.5,
            xaxis={'title': 'Жанр'},
            yaxis={'title': 'Значение'},
            plot_bgcolor='rgba(0,0,0,0)'
        )
    return fig
#Alert
@callback(
    Output('alert-container', 'children'),
    [Input('genre-dropdown', 'value'),
     Input('country-dropdown', 'value')]
)
def update_alert(selected_genres, selected_countries):
    filtered_df = df.copy()

    # Фильтрация по жанрам
    if selected_genres:
        filtered_df = filtered_df[filtered_df['genre'].isin(selected_genres)]

    # Фильтрация по странам
    if selected_countries:
        filtered_df = filtered_df[filtered_df['country'].apply(lambda x: isinstance(x, str) and any(country in x.split(', ') for country in selected_countries if isinstance(country, str)))]

    # Проверка на пустоту DataFrame после фильтрации
    if filtered_df.empty:
        return dbc.Alert(
            children=[html.H4("Фильмы не найдены!")],
            className="alert alert-dismissible alert-info",
            color="info",
            dismissable=True,
            style={'text-align': 'center'}
        )
    return None

# График-3
@callback(
    Output('scatter-plot', 'figure'),
    Input('genre-dropdown', 'value'),
    Input('country-dropdown', 'value')
)
def update_scatter_plot(selected_genres, selected_countries):
    filtered_df = df.copy()

    # Фильтрация по жанрам
    if selected_genres:
        filtered_df = filtered_df[filtered_df['genre'].isin(selected_genres)]

    # Фильтрация по странам
    if selected_countries:
        filtered_df = filtered_df[filtered_df['country'].apply(lambda x: isinstance(x, str) and any(country in x.split(', ') for country in selected_countries if isinstance(country, str)))]

    # Проверка на пустоту DataFrame после фильтрации
    if filtered_df.empty:
        return {
            'data': [],
            'layout': {
                'annotations': [{
                    'text': '',
                    'showarrow': False,
                }],
                'xaxis': {'visible': False},
                'yaxis': {'visible': False},
                'hovermode': False,
                'height': 200
            }
        }
    
    # Агрегирование данных
    agg_df = filtered_df.melt(id_vars=['genre'], value_vars=['humor', 'rhythm', 'effort', 'tension', 'erotism'])
    agg_df = agg_df.groupby(['variable', 'value']).size().reset_index(name='count')

    # Переводим английские метки в русские
    translation_dict = {
        'humor': 'Юмор',
        'rhythm': 'Ритм',
        'effort': 'Работа над фильмом',
        'tension': 'Напряжение',
        'erotism': 'Эротика'
    }

    # Применяем перевод к меткам
    agg_df['variable'] = agg_df['variable'].map(translation_dict)

    # Устанавливаем порядок характеристик
    agg_df['variable'] = pd.Categorical(agg_df['variable'], categories=['Юмор', 'Ритм', 'Работа над фильмом', 'Напряжение', 'Эротика'], ordered=True)

    # Формирование заголовка
    title = 'Характеристики фильмов'
    if selected_countries:
        title += ' от Страны производителя: ' + ', '.join(selected_countries)
    else:
        title += ' по всем странам'
    if selected_genres:
        title += ' , с Жанром: ' + ', '.join(selected_genres)
    
    fig = px.scatter(agg_df, x='variable', y='value', size='count', color='variable',
                     labels={'variable': 'Характеристики', 'value': 'Значение', 'count': 'Кол-во фильмов'},
                     title=title,
                     size_max=100)  # Увеличиваем максимальный размер пузырьков

    fig.update_layout(
        xaxis=dict(categoryorder='array', categoryarray=['Юмор', 'Ритм', 'Работа над фильмом', 'Напряжение', 'Эротика']),
        height=800  # Увеличиваем высоту графика
    )

    return fig
