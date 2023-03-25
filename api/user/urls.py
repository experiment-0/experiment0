from django.urls import path
from .views import RegistrationAPIView, EmailVerificationAPIView

urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='user_registration'),
    path('api/verify-email/<uidb64>/<token>/', EmailVerificationAPIView.as_view(), name='user_verification'),
]

# path(
#     'verify_email/<uidb64>/<token>/',
#     EmailVerify.as_view(template_name='user/verify_email.html'),
#     name='verify_email',
# ),