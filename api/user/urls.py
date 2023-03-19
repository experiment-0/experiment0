from django.urls import path, include
from django.views.generic import TemplateView
from .views import Register, EmailVerify, MyLoginView, home

urlpatterns = [

    path('login/', MyLoginView.as_view(), name='login'),
    path('', include('django.contrib.auth.urls')),
    path('home/', TemplateView.as_view(template_name='user/home.html'), name='home'),
    path('successfully_verified/', TemplateView.as_view(template_name='user/successfully_verified.html'), name='successfully_verified'),
    path(
        'invalid_verify/',
        TemplateView.as_view(template_name='user/invalid_verify.html'),
        name='invalid_verify'
    ),

    path(
        'verify_email/<uidb64>/<token>/',
        EmailVerify.as_view(template_name='user/verify_email.html'),
        name='verify_email',
    ),

    path(
        'confirm_email/',
        TemplateView.as_view(template_name='user/confirm_email.html'),
        name='confirm_email'
    ),

    path('register/', Register.as_view(template_name='user/register.html'), name='register.html',)
]
