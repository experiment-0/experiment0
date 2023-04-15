from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import BaseUser

User = get_user_model()


@admin.register(BaseUser)
class BaseUserAdminView(admin.ModelAdmin):
    list_display = ("id", "username", "email", "role")
    list_filter = ('role', )
