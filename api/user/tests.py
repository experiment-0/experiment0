from django.core import mail
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .models import BaseUser

class RegistrationTests(APITestCase):
    def test_registration(self):
        url = reverse("user_registration")
        data = {"email": "testuser@example.com", "username": "testuser", "password": "testpassword"}

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = BaseUser.objects.get(email="testuser@example.com")
        self.assertEqual(user.username, "testuser")
        self.assertFalse(user.is_active)

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Verify your email address", mail.outbox[0].subject)

    def test_email_verification(self):
        user = BaseUser.objects.create(email="testuser@example.com", username="testuser", password="testpassword")
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        verification_link = f"/api/verify-email/{uid}/{token}/"
        response = self.client.get(verification_link)

        user.refresh_from_db()
        self.assertTrue(user.mail_verified_at)
        self.assertTrue(user.is_active)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("refresh", response.data)
        self.assertIn("access", response.data)


class PerformanceTests(APITestCase):
    def test_registration_performance(self):
        url = reverse("user_registration")
        data = {"email": "testuser@example.com", "username": "testuser", "password": "testpassword"}

        start_time = time.time()
        for i in range(10):
            response = self.client.post(url, data, format="json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Elapsed time: {elapsed_time} seconds")
