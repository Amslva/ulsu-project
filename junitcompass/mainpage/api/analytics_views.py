from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Q
import json
from collections import Counter
from ..models import Vacancy


class AnalyticsAPI(APIView):
    def get(self, request):
        """API для аналитики с реальными данными"""

        vacancies = Vacancy.objects.all()
        total_vacancies = vacancies.count()

        if total_vacancies == 0:
            return Response({
                'has_data': False,
                'message': 'Нет данных для аналитики'
            })

        data = {
            'has_data': True,
            'total_vacancies': total_vacancies,
            'junior_vacancies': vacancies.filter(is_junior=True).count(),

            # Основные графики
            'top_languages': self.get_top_programming_languages(vacancies),
            'backend_frameworks': self.get_backend_frameworks(vacancies),
            'frontend_frameworks': self.get_frontend_frameworks(vacancies),
            'employment_types': self.get_employment_types(vacancies),
            'experience_levels': self.get_experience_levels(vacancies),
            'locations': self.get_top_locations(vacancies),
            'skills_analysis': self.get_skills_analysis(vacancies),

            # Статистика
            'market_stats': self.get_market_stats(vacancies)
        }

        return Response(data)

    def get_top_programming_languages(self, vacancies):
        """Топ языков программирования"""
        language_counter = Counter()
        programming_languages = [
            'python', 'javascript', 'java', 'c#', 'php', 'go', 'rust',
            'kotlin', 'swift', 'typescript', 'ruby', 'c++', 'c', 'scala'
        ]

        for vacancy in vacancies:
            text = self.get_search_text(vacancy)

            for language in programming_languages:
                if language in text:
                    language_counter[language] += 1

        # Форматируем результат
        result = [
            {'name': lang.capitalize(), 'count': count}
            for lang, count in language_counter.most_common(10)
            if count > 0  # Только языки которые есть в данных
        ]

        return result

    def get_backend_frameworks(self, vacancies):
        """Топ backend фреймворков"""
        framework_counter = Counter()
        backend_frameworks = [
            'django', 'flask', 'fastapi', 'spring', 'laravel', 'symfony',
            'node.js', 'express', 'nestjs', 'asp.net', 'ruby on rails'
        ]

        for vacancy in vacancies:
            text = self.get_search_text(vacancy)

            for framework in backend_frameworks:
                if framework in text:
                    framework_counter[framework] += 1

        return [
            {'name': self.format_framework_name(fw), 'count': count}
            for fw, count in framework_counter.most_common(8)
            if count > 0
        ]

    def get_frontend_frameworks(self, vacancies):
        """Топ frontend фреймворков"""
        framework_counter = Counter()
        frontend_frameworks = [
            'react', 'vue', 'angular', 'svelte', 'next.js', 'nuxt.js',
            'redux', 'vuex', 'jquery', 'bootstrap', 'tailwind'
        ]

        for vacancy in vacancies:
            text = self.get_search_text(vacancy)

            for framework in frontend_frameworks:
                if framework in text:
                    framework_counter[framework] += 1

        return [
            {'name': self.format_framework_name(fw), 'count': count}
            for fw, count in framework_counter.most_common(8)
            if count > 0
        ]

    def get_employment_types(self, vacancies):
        """Типы занятости"""
        employment_stats = vacancies.values('employment').annotate(
            count=Count('id')
        ).order_by('-count')

        employment_names = {
            'full': 'Полная занятость',
            'part': 'Частичная занятость',
            'project': 'Проектная работа',
            'remote': 'Удаленная работа',
            'probation': 'Стажировка'
        }

        return [
            {
                'employment_type': item['employment'],
                'name': employment_names.get(item['employment'], item['employment']),
                'count': item['count']
            }
            for item in employment_stats
        ]

    def get_experience_levels(self, vacancies):
        """Уровни опыта"""
        experience_stats = vacancies.values('experience').annotate(
            count=Count('id')
        ).order_by('-count')

        experience_names = {
            'noExperience': 'Без опыта',
            'between1And3': '1-3 года',
            'between3And6': '3-6 лет',
            'moreThan6': 'Более 6 лет'
        }

        return [
            {
                'experience': item['experience'],
                'name': experience_names.get(item['experience'], item['experience']),
                'count': item['count']
            }
            for item in experience_stats
        ]

    def get_top_locations(self, vacancies):
        """Топ локаций"""
        location_stats = vacancies.values('location').annotate(
            count=Count('id')
        ).order_by('-count')[:8]

        return list(location_stats)

    def get_skills_analysis(self, vacancies):
        """Анализ навыков"""
        all_skills = []

        for vacancy in vacancies:
            try:
                skills = json.loads(vacancy.key_skills)
                all_skills.extend(skills)
            except:
                continue

        skill_counter = Counter(all_skills)

        return [
            {'skill': skill, 'count': count}
            for skill, count in skill_counter.most_common(15)
        ]

    def get_market_stats(self, vacancies):
        """Общая статистика рынка"""
        total = vacancies.count()
        junior_count = vacancies.filter(is_junior=True).count()

        return {
            'junior_percentage': round((junior_count / total) * 100, 1) if total > 0 else 0,
            'remote_percentage': self.calculate_remote_percentage(vacancies),
            'top_technologies': self.get_top_technologies_summary(vacancies)
        }

    def calculate_remote_percentage(self, vacancies):
        """Процент удаленных вакансий"""
        remote_count = vacancies.filter(
            Q(schedule='remote') | Q(location__icontains='удален')
        ).count()
        total = vacancies.count()
        return round((remote_count / total) * 100, 1) if total > 0 else 0

    def get_top_technologies_summary(self, vacancies):
        """Сводка по технологиям"""
        technologies = ['python', 'javascript', 'java', 'react', 'django', 'spring']
        summary = {}

        for tech in technologies:
            count = vacancies.filter(
                Q(title__icontains=tech) |
                Q(description__icontains=tech) |
                Q(key_skills__icontains=tech)
            ).count()
            summary[tech] = count

        return summary

    def get_search_text(self, vacancy):
        """Получить текст для поиска технологий"""
        description = vacancy.description.lower()

        try:
            key_skills = json.loads(vacancy.key_skills)
            skills_text = ' '.join(key_skills).lower()
        except:
            skills_text = ''

        return f"{vacancy.title.lower()} {description} {skills_text}"

    def format_framework_name(self, framework):
        """Форматирование названий фреймворков"""
        names = {
            'node.js': 'Node.js',
            'next.js': 'Next.js',
            'nuxt.js': 'Nuxt.js',
            'ruby on rails': 'Ruby on Rails',
            'asp.net': 'ASP.NET'
        }
        return names.get(framework, framework.capitalize())