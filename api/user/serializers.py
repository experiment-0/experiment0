from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Student, SchoolAdmin

User = get_user_model()


class StudentRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = Student
        fields = ['email', 'username', 'password', 'is_student']
        extra_kwargs = {"password": {"write_only": True}}


class SchoolAdminRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = SchoolAdmin
        fields = ['email', 'username', 'password', 'is_student']
        extra_kwargs = {"password": {"write_only": True}}
