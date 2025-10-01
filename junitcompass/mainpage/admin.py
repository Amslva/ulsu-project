from django.contrib import admin
from .models import Profession, Category

@admin.register(Profession)
class ProfessionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title", )}
    list_display = ('id','title','time_create', 'is_published', 'cat')
    list_display_links = ('id', 'title')
    ordering = ['time_create', 'title']
    list_editable = ('is_published', 'cat' )
    list_per_page = 10
    search_fields = ['title']
    list_filter = ['cat__name', 'is_published']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    list_display_links = ('id','name')
    ordering = ['name']
