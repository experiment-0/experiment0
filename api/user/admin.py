from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import BaseUser, Student, SchoolAdmin


User = get_user_model()
admin.site.register(BaseUser)
admin.site.register(Student)
admin.site.register(SchoolAdmin)
