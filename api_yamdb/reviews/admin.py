from django.contrib import admin

from api_yamdb.settings import EMPTY_VALUE_FOR_ADMIN_PY
from . import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug'
    )
    list_editable = ('name', 'slug')
    search_fields = ('id', 'name', 'slug',)
    list_filter = ('name', 'slug',)
    empty_value_display = EMPTY_VALUE_FOR_ADMIN_PY


@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug'
    )
    list_editable = ('name', 'slug')
    search_fields = ('id', 'name', 'slug',)
    list_filter = ('name', 'slug',)
    empty_value_display = EMPTY_VALUE_FOR_ADMIN_PY


@admin.register(models.Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'year',
        'category'
    )
    list_editable = ('name', 'year', 'category')
    search_fields = ('id', 'name', 'year',)
    list_filter = ('name', 'year',)
    empty_value_display = EMPTY_VALUE_FOR_ADMIN_PY


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'text',
        'pub_date',
        'author',
        'score',
    )
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = EMPTY_VALUE_FOR_ADMIN_PY


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'review',
        'author',
        'text',
        'pub_date',
    )
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = EMPTY_VALUE_FOR_ADMIN_PY
