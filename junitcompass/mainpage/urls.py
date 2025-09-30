from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),  # http://127.0.0.1:8000
    path('stats/', views.analyze, name='stats'),
    path('login/', views.login, name='login'),
    path('post/<slug:post_slug>/', views.show_post, name='post'),
    path('category/<slug:cat_slug>/', views.show_category, name='category'),
]
