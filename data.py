import pandas as pd

#df = pd.read_csv('filmtv_movies.csv', sep=',')
df = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vQEorO3xoyMmm8yUYsEy6VyOLztlwl8EA_qPalSZ92_ORz45EhS7FV8dXXrQbtsIXN_94cvEMLVsWuX/pub?output=csv", sep=',')

all_g = df['genre'].dropna().unique()
all_year = df['year'].dropna().unique()
directors = df['directors'].dropna().str.split(', ').explode().unique()
all_cont = df['country'].dropna().str.split(', ').explode().unique()
avg_vote = df['avg_vote'].dropna().unique()
avg_vote = sorted(avg_vote)

# 1. Средняя оценка критиков по жанру
critics_avg_by_genre = df.groupby('genre')['critics_vote'].mean().round(1)

# 2. Средняя оценка зрителей по жанру
public_avg_by_genre = df.groupby('genre')['public_vote'].mean().round(1)

# 3. Средняя продолжительность фильмов по жанру
duration_avg_by_genre = df.groupby('genre')['duration'].mean().round(1)

# 4. Количество фильмов в каждом жанре
film_count_by_genre = df['genre'].explode().value_counts().sort_index()

# Вывод результатов

# Проверка результата
#print(all_count)
#print(all_cont)
#print(df.columns)
#print(sorted(avg_vote))
#print('avg_vote' in df.columns)
#print(df['avg_vote'].dtype) 
#print(df['avg_vote'].max())
#print(film_count_by_genre)