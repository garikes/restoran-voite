import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ..models import Employee


class RegisterAPIViewTest(APITestCase):
    url = reverse('register')

    def test_register_employee_valid_data(self):
        valid_employee_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'password': 'secret_password!!@#1234324',
            'phone': '1234567890',
        }

        response = self.client.post(self.url, data=valid_employee_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], status.HTTP_200_OK)

        self.assertTrue(Employee.objects.filter(username='johndoe').exists())

    def test_register_employee_invalid_data(self):
        invalid_employee_data = {
            'first_name': 'Jane',
            'email': 'janedoe@example.com',
            'password': 'secret_password!!@#1234324',
        }

        response = self.client.post(self.url, data=invalid_employee_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['success'], False)
        self.assertIn('last_name', response.data['data'])

        self.assertFalse(Employee.objects.filter(username='janedoe').exists())
