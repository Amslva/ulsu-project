from django.urls import path
from . import views
from .api import views as api_views

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),  # http://127.0.0.1:8000
    path('stats/', views.analyze, name='stats'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', views.ShowCategory.as_view(), name='category'),

    path('api/categories/', api_views.CategoryListAPI.as_view(), name='api_categories'),
    path('api/professions/', api_views.ProfessionListAPI.as_view(), name='api_professions'),
    path('api/professions/category/<int:category_id>/', api_views.ProfessionByCategoryAPI.as_view(),
         name='api_professions_by_category'),
    path('api/analytics/stats/', api_views.AnalyticsStatsAPI.as_view(), name='api_analytics'),
]
