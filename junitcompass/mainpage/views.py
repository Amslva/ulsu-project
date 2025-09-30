from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render,  get_object_or_404

from mainpage.models import Profession, Category

menu = [{'title': "Главная страница", 'url_name': 'home'},
    {'title': "Перейти к аналитике", 'url_name': 'stats'},
        {'title': "Войти", 'url_name': 'login'}
]


def index(request):
    posts = Profession.published.all()
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0,
    }
    return render(request, 'mainpage/index.html', context=data)


def analyze (request):
    return render(request, 'mainpage/analyze.html', {'title': 'Analyze', 'menu': menu})

def login(request):
    return HttpResponse("Авторизация")


def show_post(request, post_slug):
    post = get_object_or_404(Profession, slug=post_slug)

    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1,
    }
    return render(request, 'mainpage/post.html', context=data)

def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Profession.published.filter(cat_id=category.pk)

    data = {
        'title': f'Направление: {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected':category.pk,
    }

    return render(request, 'mainpage/index.html', context=data)


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена:(</h1>')

