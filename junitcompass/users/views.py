from django.contrib.auth import  logout
from django.contrib.auth.views import LoginView, LogoutView
from django.http import  HttpResponseRedirect
from django.urls import reverse

from users.forms import LoginUserForm


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}

