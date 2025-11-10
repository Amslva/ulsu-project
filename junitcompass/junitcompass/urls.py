from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('mainpage.urls')),
    path("__debug__/", include("debug_toolbar.urls")),
]
