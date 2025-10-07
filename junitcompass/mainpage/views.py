from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render,  get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView

from mainpage.models import Profession, Category

menu = [{'title': "Главная страница", 'url_name': 'home'},
    {'title': "Перейти к аналитике", 'url_name': 'stats'},
]


class HomePage(ListView):
    template_name = 'mainpage/index.html'
    context_object_name = 'posts'
    extra_context = {
        'title': 'Главная страница',
        'menu': menu,
    }
    def get_queryset(self):
        return Profession.published.all()


def analyze (request):
    return render(request, 'mainpage/analyze.html', {'title': 'Analyze', 'menu': menu})


def login(request):
    return HttpResponse("Авторизация")


class ShowPost(DetailView):
    model = Profession
    template_name = 'mainpage/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post'].title
        return context
    def det_object(self, post):
        return get_object_or_404(Profession.published, slug=self.kwargs[self.slug_url_kwarg])


class ShowCategory(ListView):
    template_name = 'mainpage/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Profession.published.filter(cat__slug=self.kwargs['cat_slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        context['title'] = 'Категория - ' + cat.name
        context['cat_selected'] = cat.pk
        return context


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена:(</h1>')

