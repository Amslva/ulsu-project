from django.contrib import admin
from django.urls import path, include
from mainpage import views


urlpatterns = [
    path('admin/', admin.site.urls),#http://127.0.0.1:8000/admin/
    path('', include('mainpage.urls')), #http://127.0.0.1:8000
    path('users/', include('users.urls', namespace='users')),
    path("__debug__/", include("debug_toolbar.urls")),
]

handler404 = views.page_not_found


admin.site.site_header = "Панель администрирования"
admin.site.index_title = "JunItCompass"