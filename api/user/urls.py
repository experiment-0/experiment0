from django.urls import path
from .views import RegistrationAPIView, EmailVerificationAPIView, LoginAPIView, LogoutAPIView

urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='user_registration'),
    path('verify-email/<uidb64>/<token>/', EmailVerificationAPIView.as_view(), name='user_verification'),
    path('login/', LoginAPIView.as_view(), name='user_login'),
    path('logout/', LogoutAPIView.as_view(), name='user_logout'),
]
