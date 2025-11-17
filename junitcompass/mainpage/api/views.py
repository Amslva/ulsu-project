from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Profession, Category

class CategoryListAPI(APIView):
    def get(self, request):
        categories = Category.objects.all()
        data = [
            {
                'id': category.id,
                'name': category.name,
                'slug': category.slug
            }
            for category in categories
        ]
        return Response(data)

class ProfessionListAPI(APIView):
    def get(self, request):
        professions = Profession.objects.filter(is_published=True)
        data = [
            {
                'id': prof.id,
                'title': prof.title,
                'slug': prof.slug,
                'time_create': prof.time_create,
                'time_update': prof.time_update,
                'cat_id': prof.cat_id,
                'cat_name': prof.cat.name
            }
            for prof in professions
        ]
        return Response(data)

class ProfessionByCategoryAPI(APIView):
    def get(self, request, category_id):
        try:
            professions = Profession.objects.filter(cat_id=category_id, is_published=True)
            data = [
                {
                    'id': prof.id,
                    'title': prof.title,
                    'slug': prof.slug,
                    'cat_id': prof.cat_id,
                    'cat_name': prof.cat.name
                }
                for prof in professions
            ]
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

class AnalyticsStatsAPI(APIView):
    def get(self, request):
        data = {
            'top_languages': [
                {'name': 'Python', 'count': 45},
                {'name': 'JavaScript', 'count': 38},
                {'name': 'Java', 'count': 32}
            ],
            'backend_frameworks': [
                {'name': 'Django', 'count': 28},
                {'name': 'Spring', 'count': 25},
                {'name': 'ASP.NET', 'count': 22}
            ]
        }
        return Response(data)

class ProfessionDetailAPI(APIView):
    def get(self, request, slug):
        try:
            profession = Profession.objects.get(slug=slug, is_published=True)
            data = {
                'id': profession.id,
                'title': profession.title,
                'slug': profession.slug,
                'content': profession.content,  # ← ВОТ КОНТЕНТ!
                'time_create': profession.time_create,
                'time_update': profession.time_update,
                'cat_id': profession.cat_id,
                'cat_name': profession.cat.name
            }
            return Response(data)
        except Profession.DoesNotExist:
            return Response({'error': 'Профессия не найдена'}, status=404)