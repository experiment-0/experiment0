from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from user.models import BaseUser
from user.serializers import BaseUserRegistrationSerializer
# import requests
# import string
# import random
# import time
# import unittest

User = get_user_model()


class BaseUserModelTestCase(TestCase):
    def setUp(self):
        self.user = BaseUser.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="testpassword"
        )

    def test_create_user(self):
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(self.user.username, "testuser")
        self.assertTrue(self.user.check_password("testpassword"))

    def test_create_superuser(self):
        superuser = BaseUser.objects.create_superuser(
            email="superuser@example.com",
            username="superuser",
            password="superpassword"
        )
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_missing_email(self):
        with self.assertRaises(ValueError):
            BaseUser.objects.create_user(
                email=None,
                username="testuser",
                password="testpassword"
            )

    def test_missing_username(self):
        with self.assertRaises(ValueError):
            BaseUser.objects.create_user(
                email="test@example.com",
                username=None,
                password="testpassword"
            )


class BaseUserRegistrationSerializerTestCase(TestCase):
    def test_valid_data(self):
        data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpassword"
        }
        serializer = BaseUserRegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_missing_email(self):
        data = {
            "username": "testuser",
            "password": "testpassword"
        }
        serializer = BaseUserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

    def test_missing_username(self):
        data = {
            "email": "test@example.com",
            "password": "testpassword"
        }
        serializer = BaseUserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("username", serializer.errors)

    def test_missing_password(self):
        data = {
            "email": "test@example.com",
            "username": "testuser",
        }
        serializer = BaseUserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)


class RegistrationTests(APITestCase):
    def test_create_user(self):
        """Какой-то очень долгий тест"""

        url = reverse('user_registration')
        data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'password123',
            'role': 'St',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')
        self.assertEqual(User.objects.get().email, 'test@example.com')

    def test_create_user_with_existing_email(self):
        BaseUser.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='password123',
            role='St',
        )
        url = reverse('user_registration')
        data = {
            'email': 'test@example.com',
            'username': 'testuser2',
            'password': 'password123',
            'role': 'St',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_missing_fields(self):
        url = reverse('user_registration')
        data = {
            'email': 'test@example.com',
            'password': 'password123',
            'role': 'St',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_email_verification(self):
        user = BaseUser.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='password123',
            role='St',
        )
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        url = reverse('user_verification', args=[uid, token])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertIsNotNone(user.mail_verified_at)


class EmailVerificationAPIViewTests(APITestCase):
    def setUp(self):
        self.user = BaseUser.objects.create_user(
            username='test_user',
            email='test@example.com',
            password='test_password'
        )
        self.token = default_token_generator.make_token(self.user)
        self.uid = str(self.user.pk)
        self.uidb64 = urlsafe_base64_encode(self.uid.encode())

    def test_email_verification_successful(self):
        url = reverse('user_verification', args=[self.uidb64, self.token])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertIsNotNone(self.user.mail_verified_at)

    def test_email_verification_fails_with_invalid_token(self):
        token = default_token_generator.make_token(BaseUser())
        uid = str(self.user.pk)
        uidb64 = urlsafe_base64_encode(uid.encode())
        url = reverse('user_verification', args=[uidb64, token])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertIsNone(self.user.mail_verified_at)


# class TestRegistrationAndEmailVerificationAPI(unittest.TestCase):
#     def setUp(self):
#         self.base_url = "http://localhost:8000"
#         self.emails = []
#         self.tokens = []
#
#     def test_registration_and_email_verification(self):
#         for i in range(100):
#             email = f"test-{i}@example.com"
#             password = "".join(random.choices(string.ascii_letters + string.digits, k=8))
#             data = {
#                 "email": email,
#                 "password": password,
#                 "password_confirmation": password,
#             }
#
#             # Register a new user
#             response = requests.post(f"{self.base_url}/user/register/", data=data)
#             self.assertEqual(response.status_code, 201)
#
#             # Verify the email address of the new user
#             uid = response.json()["uid"]
#             token = response.json()["token"]
#             url = f"{self.base_url}/user/verify-email/{uid}/{token}/"
#             response = requests.get(url)
#             self.assertEqual(response.status_code, 200)
#
#             # Save the email and token for future reference
#             self.emails.append(email)
#             self.tokens.append(token)
#
#             # Sleep for a random interval to simulate realistic user behavior
#             time.sleep(random.uniform(0.5, 2.0))
#
#     def tearDown(self):
#         # Clean up the registered users by deleting them
#         for email, token in zip(self.emails, self.tokens):
#             uid = requests.utils.urlsafe_base64_encode(email.encode())
#             url = f"{self.base_url}/user/delete/{uid}/{token}/"
#             requests.delete(url)
