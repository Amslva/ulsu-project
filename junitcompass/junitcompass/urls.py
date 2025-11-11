from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.shortcuts import redirect

def redirect_to_frontend(request):
    return redirect('http://localhost:3000/')

urlpatterns = [
    path('', redirect_to_frontend),
    path('admin/', admin.site.urls),
    path('api/', include('mainpage.urls')),
    path("__debug__/", include("debug_toolbar.urls")),
]
