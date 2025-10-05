### Инструкция:
1) Клонирование репозитория ```git clone https://github.com/Amslva/ulsu-project.git```
2) Создание виртуального окружения ```python -m venv YOUR_NAME_VENV``` для создания виртуального 
окружения с именем YOUR_NAME_VENV в текущей папке
3) Активация окружения ```.\YOUR_NAME_VENV\Scripts\activate```
После активации в командной строке должно отображаться (YOUR_NAME_VENV)
4) Установка зависимостей ```pip install -r requirements.txt```
5) Применение миграций ```python manage.py migrate```
6) Запуск ```python manage.py runserver```

Полезные ссылки: 
* [Clone and Run a Django Project](https://www.codespeedy.com/clone-and-run-a-django-project-from-github/)
* [Django documentation](https://docs.djangoproject.com/en/5.2/)
