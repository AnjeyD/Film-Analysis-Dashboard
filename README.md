# Film Analysis Dashboard
Многостраничный дашборд для анализа фильмов с использованием данных из датасета FilmTV на платформе Kaggle <!-- описание репозитория -->

Этот проект представляет собой веб-приложение для подбора и анализа фильмов, созданное с использованием фреймворка Dash. Приложение включает несколько страниц, где пользователи могут искать фильмы, просматривать топ-10 фильмов и анализировать статистику.

## Оглавление

- [Установка](#установка)
- [Запуск приложения](#запуск-приложения)
- [Структура проекта](#структура-проекта)
- [Использование](#использование)
- [Автор](#автор)

## Установка

1. Склонируйте репозиторий:
    ```sh
    git clone https://github.com/ваш_пользователь/movie-recommendation-dashboard.git
    ```

2. Перейдите в директорию проекта:
    ```sh
    cd movie-recommendation-dashboard
    ```

3. Создайте виртуальное окружение и активируйте его:
    ```sh
    python -m venv venv
    source venv/bin/activate  # Для Windows: venv\Scripts\activate
    ```

4. Установите необходимые зависимости:
    ```sh
    pip install -r requirements.txt
    ```

## Запуск приложения

После установки всех зависимостей, вы можете запустить приложение командой:
```sh
python app.py

## Структура проекта

```plaintext
├── app.py                 # Главный файл приложения, содержащий настройки и маршрутизацию
├── requirements.txt       # Файл зависимостей проекта
└── pages/                 # Директория с файлами страниц
    ├── amain.py           # Главная страница
    ├── kinopoisk.py       # Страница подбора фильмов
    ├── topfilm.py         # Страница с топ-10 фильмами
    └── xstatistics.py     # Страница статистики

## Использование

Приложение состоит из нескольких страниц:

- **Главная**: Основная информация о приложении.
- **Подбор фильма**: Позволяет пользователям искать фильмы по различным критериям.
- **Топ-10**: Отображает топ-10 популярных фильмов.
- **Статистика**: Предоставляет различные статистические данные о фильмах.

Для навигации используйте боковую панель меню, как раз таки содержащее эти страницы.