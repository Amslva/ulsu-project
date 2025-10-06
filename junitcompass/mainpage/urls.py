from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),  # http://127.0.0.1:8000
    path('stats/', views.analyze, name='stats'),
    path('login/', views.login, name='login'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', views.ShowCategory.as_view(), name='category'),
]
