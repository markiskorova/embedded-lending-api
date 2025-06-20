from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

class RegisterTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_user(self):
        data = {
            "username": "testuser",
            "password": "securepass123",
            "company_name": "TestCorp"
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
