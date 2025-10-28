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

#temporary
class ProfessionByCategoryAPI(APIView):
    def get(self, request, category_id):
        professions = Profession.objects.filter(cat_id=category_id, is_published=True)
        data = [
            {
                'id': prof.id,
                'title': prof.title,
                'slug': prof.slug,
                'cat_id': prof.cat_id
            }
            for prof in professions
        ]
        return Response(data)

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