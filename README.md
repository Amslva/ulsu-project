Инструкция:
1) Клонирование репозитория ```git clone https://github.com/Amslva/ulsu-project.git```
2) Создание виртуального окружения ```python -m venv YOUR_NAME_VENV``` для создания виртуального 
окружения с именем YOUR_NAME_VENV в текущей папке
3) Активация окружения ```.\YOUR_NAME_VENV\Scripts\activate```
После активации в командной строке должно отображаться (YOUR_NAME_VENV)
4) Установка Django (в корневой папке проекта) ```pip install django==5.2.7```
5) Установка зависимостей ```pip install -r requirements.txt```
6) Применение миграций ```python manage.py makemigrations```, ```python manage.py migrate```
7) Запуск ```python manage.py runserver```

Полезная ссылка: [Clone and Run a Django Project](https://www.codespeedy.com/clone-and-run-a-django-project-from-github/)