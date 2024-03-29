from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse("user:create")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        email = "teste@example.com"
        password = "teste123"
        payload = {
            "email": email,
            "password": password,
            "name": "Teste",
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email="teste@example.com")
        self.assertTrue(user.check_password(password))
        self.assertNotIn("password", res.data)

    def test_user_with_email_exists_error(self):
        payload = {
            "email": "teste@example.com",
            "password": "teste123",
            "name": "Teste",
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_with_short_password_error(self):
        payload = {
            "email": "test@example.com",
            "password": "123",
            "name": "Teste",
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = (
            get_user_model().objects.filter(email=payload["email"]).exists()
        )  # noqa
        self.assertFalse(user_exists)
