import requests
import time
import json
from datetime import datetime
from django.core.management.base import BaseCommand
from django.db import transaction
from mainpage.models import Vacancy


class Command(BaseCommand):
    help = 'Парсинг вакансий с HH.ru для аналитики'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=50, help='Количество вакансий для сбора')
        parser.add_argument('--delay', type=float, default=0.1, help='Задержка между запросами')

    def handle(self, *args, **options):
        self.stdout.write("Запуск парсера вакансий HH.ru...")

        vacancies_count = self.parse_and_save_vacancies(
            total_vacancies=options['count'],
            delay=options['delay']
        )

        self.stdout.write(self.style.SUCCESS(f"Собрано и сохранено {vacancies_count} вакансий"))

    def parse_and_save_vacancies(self, total_vacancies=50, delay=0.1):

        search_queries = [
            "junior python", "junior javascript", "junior java",
            "стажер программист", "начальный разработчик",
            "data scientist junior", "qa junior", "devops junior"
        ]

        all_vacancies = []

        for query in search_queries:
            if len(all_vacancies) >= total_vacancies:
                break

            self.stdout.write(f"Поиск: '{query}'")

            page = 0
            while len(all_vacancies) < total_vacancies:
                vacancies = self.search_vacancies(query, page)
                if not vacancies:
                    break

                for vacancy_data in vacancies:
                    if len(all_vacancies) >= total_vacancies:
                        break

                    vacancy_details = self.get_vacancy_details(vacancy_data['id'])
                    if vacancy_details:
                        processed_vacancy = self.process_vacancy(vacancy_details, query)
                        if processed_vacancy:
                            all_vacancies.append(processed_vacancy)

                            progress = len(all_vacancies) / total_vacancies * 100
                            self.stdout.write(f"Прогресс: {len(all_vacancies)}/{total_vacancies} ({progress:.1f}%)",
                                              ending='\r')

                    time.sleep(delay)

                page += 1
                if page >= 10:
                    break

        saved_count = self.save_vacancies_to_db(all_vacancies)
        return saved_count

    def search_vacancies(self, query, page=0):
        url = "https://api.hh.ru/vacancies"
        params = {
            'text': query,
            'experience': 'noExperience',
            'per_page': 20,
            'page': page,
            'area': 1,
            'only_with_salary': True
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get('items', [])
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ошибка поиска: {e}"))
            return []

    def get_vacancy_details(self, vacancy_id):
        url = f"https://api.hh.ru/vacancies/{vacancy_id}"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ошибка получения вакансии {vacancy_id}: {e}"))
            return None

    def process_vacancy(self, vacancy_data, search_query):

        key_skills = [skill['name'] for skill in vacancy_data.get('key_skills', [])]

        is_junior = self.is_junior_vacancy(vacancy_data)


        salary = vacancy_data.get('salary', {})

        return {
            'hh_id': vacancy_data['id'],
            'title': vacancy_data['name'],
            'description': vacancy_data.get('description', '')[:5000],
            'url': vacancy_data.get('alternate_url', ''),
            'published_at': vacancy_data.get('published_at'),
            'experience': vacancy_data.get('experience', {}).get('id', 'noExperience'),
            'employment': vacancy_data.get('employment', {}).get('id', 'full'),
            'schedule': vacancy_data.get('schedule', {}).get('id', 'fullDay'),
            'location': vacancy_data.get('area', {}).get('name', ''),
            'company_name': vacancy_data.get('employer', {}).get('name', ''),
            'company_url': vacancy_data.get('employer', {}).get('alternate_url', ''),
            'salary_from': salary.get('from'),
            'salary_to': salary.get('to'),
            'salary_currency': salary.get('currency'),
            'key_skills': json.dumps(key_skills, ensure_ascii=False),
            'is_junior': is_junior,
            'search_query': search_query,
        }

    def is_junior_vacancy(self, vacancy_data):

        name = vacancy_data.get('name', '').lower()
        description = vacancy_data.get('description', '').lower()

        junior_keywords = [
            'junior', 'trainee', 'стажер', 'начальный', 'младший',
            'без опыта', 'нет опыта', 'начало карьеры', 'студент'
        ]

        text_to_check = f"{name} {description}"
        return any(keyword in text_to_check for keyword in junior_keywords)

    @transaction.atomic
    def save_vacancies_to_db(self, vacancies_data):

        saved_count = 0

        for vacancy_data in vacancies_data:
            try:

                vacancy, created = Vacancy.objects.update_or_create(
                    hh_id=vacancy_data['hh_id'],
                    defaults=vacancy_data
                )
                saved_count += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Ошибка сохранения вакансии: {e}"))

        return saved_count