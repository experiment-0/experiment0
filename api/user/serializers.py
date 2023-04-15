from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import BaseUser

User = get_user_model()


class BaseUserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = BaseUser
        fields = ['email', 'username', 'password', 'role']
        extra_kwargs = {"password": {"write_only": True}}
