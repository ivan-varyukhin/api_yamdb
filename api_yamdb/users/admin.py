from django.contrib import admin

from api_yamdb.settings import EMPTY_VALUE_FOR_ADMIN_PY
from .models import User


@admin.register(User)
class User(admin.ModelAdmin):
    list_display = ('username', 'email', 'confirmation_code', 'role')
    search_fields = ('username', 'email',)
    list_filter = ('role',)
    empty_value_display = EMPTY_VALUE_FOR_ADMIN_PY
