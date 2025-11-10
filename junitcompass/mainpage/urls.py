from django.urls import path
from .api import views as api_views
from .api.auth_views import RegisterAPI, LoginAPI, LogoutAPI, UserProfileAPI

urlpatterns = [
    path('categories/', api_views.CategoryListAPI.as_view(), name='api_categories'),
    path('professions/', api_views.ProfessionListAPI.as_view(), name='api_professions'),
    path('professions/category/<int:category_id>/', api_views.ProfessionByCategoryAPI.as_view(),
         name='api_professions_by_category'),
    path('analytics/stats/', api_views.AnalyticsStatsAPI.as_view(), name='api_analytics'),

    path('auth/register/', RegisterAPI.as_view(), name='api_register'),
    path('auth/login/', LoginAPI.as_view(), name='api_login'),
    path('auth/logout/', LogoutAPI.as_view(), name='api_logout'),
    path('auth/profile/', UserProfileAPI.as_view(), name='api_profile'),
]