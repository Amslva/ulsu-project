import os
import django
import sys

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'junitcompass.settings')
django.setup()

from mainpage.models import Category, Profession
from django.utils import timezone

def create_categories():
    categories_data = [
        {'name': 'Веб-разработка', 'slug': 'web-development'},
        {'name': 'Мобильная разработка', 'slug': 'mobile-development'},
        {'name': 'Разработка игр', 'slug': 'game-development'},
        {'name': 'Data Science & AI', 'slug': 'data-science-ai'},
        {'name': 'Кибербезопасность', 'slug': 'cybersecurity'},
        {'name': 'Тестирование (QA)', 'slug': 'qa'},
        {'name': 'Администрирование & DevOps', 'slug': 'devops'},
        {'name': 'Менеджмент', 'slug': 'project-management'},
        {'name': 'Аналитика данных', 'slug': 'data-analytics'},
        {'name': 'Техническая поддержка', 'slug': 'support'},
    ]
    
    categories = {}
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'slug': cat_data['slug']}
        )
        categories[cat_data['name']] = category
        print(f"Категория: {category.name} - {'создана' if created else 'уже существует'}")
    
    return categories

def create_professions(categories):
    professions_data = [
        {
            'title': 'Frontend разработчик',
            'slug': 'frontend-developer',
            'content': 'Создает пользовательский интерфейс веб-сайтов и приложений. Работает с HTML, CSS, JavaScript и современными фреймворками.',
            'category': 'Веб-разработка'
        },
        {
            'title': 'Backend разработчик',
            'slug': 'backend-developer',
            'content': 'Разрабатывает серверную часть веб-приложений. Работает с базами данных, API и бизнес-логикой.',
            'category': 'Веб-разработка'
        },
        {
            'title': 'Fullstack разработчик',
            'slug': 'fullstack-developer',
            'content': 'Универсальный специалист, работающий как с фронтендом, так и с бэкендом веб-приложений.',
            'category': 'Веб-разработка'
        },
        {
            'title': 'Data Scientist',
            'slug': 'data-scientist',
            'content': 'Анализирует большие данные, строит модели машинного обучения и извлекает ценную информацию для бизнеса.',
            'category': 'Data Science & AI'
        },
        {
            'title': 'Machine Learning Engineer',
            'slug': 'ml-engineer',
            'content': 'Разрабатывает и внедряет модели машинного обучения в производственные системы.',
            'category': 'Data Science & AI'
        },
        {
            'title': 'Специалист по кибербезопасности',
            'slug': 'cybersecurity-specialist',
            'content': 'Защищает информационные системы, сети и данные от цифровых угроз и атак. Обеспечивает конфиденциальность, целостность и доступность информации.',
            'category': 'Кибербезопасность'
        },
        {
            'title': 'Penetration Tester',
            'slug': 'penetration-tester',
            'content': 'Проводит тестирование на проникновение, находит уязвимости в системах безопасности организации.',
            'category': 'Кибербезопасность'
        },
        {
            'title': 'DevOps инженер',
            'slug': 'devops-engineer',
            'content': 'Автоматизирует процессы разработки, тестирования и развертывания приложений. Работает с CI/CD, контейнеризацией и облачными системами.',
            'category': 'Администрирование & DevOps'
        },
        {
            'title': 'Android разработчик',
            'slug': 'android-developer',
            'content': 'Создает приложения для операционной системы Android на Java или Kotlin.',
            'category': 'Мобильная разработка'
        },
        {
            'title': 'iOS разработчик',
            'slug': 'ios-developer',
            'content': 'Разрабатывает приложения для устройств Apple на Swift или Objective-C.',
            'category': 'Мобильная разработка'
        },
        {
            'title': 'QA инженер',
            'slug': 'qa-engineer',
            'content': 'Обеспечивает качество программного обеспечения через тестирование и автоматизацию процессов.',
            'category': 'Тестирование (QA)'
        },
        {
            'title': 'Системный администратор',
            'slug': 'system-administrator',
            'content': 'Управляет IT-инфраструктурой компании: серверами, сетями, пользователями и системами резервного копирования.',
            'category': 'Администрирование & DevOps'
        },
        {
            'title': 'Project Manager',
            'slug': 'project-manager',
            'content': 'Управляет IT-проектами: планирует сроки, распределяет ресурсы и контролирует выполнение задач.',
            'category': 'Менеджмент'
        },
        {
            'title': 'Data Analyst',
            'slug': 'data-analyst',
            'content': 'Анализирует данные для поддержки бизнес-решений, создает отчеты и визуализации.',
            'category': 'Аналитика данных'
        },
        {
            'title': 'Специалист технической поддержки',
            'slug': 'technical-support-specialist',
            'content': 'Оказывает помощь пользователям в решении технических проблем с программным обеспечением и IT-оборудованием.',
            'category': 'Техническая поддержка'
        },
    ]
    
    for prof_data in professions_data:
        profession, created = Profession.objects.get_or_create(
            title=prof_data['title'],
            defaults={
                'slug': prof_data['slug'],
                'content': prof_data['content'],
                'cat': categories[prof_data['category']],
                'is_published': True
            }
        )
        print(f"Профессия: {profession.title} - {'создана' if created else 'уже существует'}")

if __name__ == '__main__':
    print("Создание категорий...")
    categories = create_categories()
    
    print("\nСоздание профессий...")
    create_professions(categories)
    
    print("\nГотово! Данные успешно добавлены в базу.")