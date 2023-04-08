from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils import timezone
from django.core.mail import send_mail
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import BaseUser
from .serializers import SchoolAdminRegistrationSerializer, StudentRegistrationSerializer


class RegistrationAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        is_student = request.data.get('is_student')
        if is_student == 'True':
            serializer = StudentRegistrationSerializer(data=request.data)
        else:
            serializer = SchoolAdminRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        verification_link = f"{request.scheme}://{request.get_host()}/api/verify-email/{uid}/{token}/"
        message = f"Please verify your email address by clicking the link below:\n\n{verification_link}"
        send_mail(
            "Verify your email address",
            message,
            "noreply@example.com",
            [user.email],
            fail_silently=False,
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EmailVerificationAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = BaseUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, BaseUser.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            user.mail_verified_at = timezone.now()
            user.save()
            refresh = RefreshToken.for_user(user)
            return Response(
                {"refresh": str(refresh), "access": str(refresh.access_token)},
                status=status.HTTP_200_OK,
            )

        return Response(status=status.HTTP_400_BAD_REQUEST)
