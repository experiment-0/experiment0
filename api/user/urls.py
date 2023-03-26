from django.urls import path
from .views import RegistrationAPIView, EmailVerificationAPIView

urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='user_registration'),
    path('api/verify-email/<uidb64>/<token>/', EmailVerificationAPIView.as_view(), name='user_verification'),
]
