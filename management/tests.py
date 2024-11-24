from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Employee


class EmployeeAPITestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            'admin', 'admin@test.com', 'password'
        )
        self.normal_user = User.objects.create_user(
            'user', 'user@test.com', 'password'
        )
        self.employee = Employee.objects.create(
            name="John Doe",
            email="johndoe@example.com",
            position="Developer"
        )
        self.client.login(username='admin', password='password')

    def test_list_employees(self):
        response = self.client.get('/employees/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_employee(self):
        data = {
            "name": "Jane Smith",
            "email": "janesmith@example.com",
            "position": "Manager"
        }
        response = self.client.post('/employees/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_employee(self):
        data = {"name": "John Updated"}
        response = self.client.patch(f'/employees/{self.employee.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_employee(self):
        response = self.client.delete(f'/employees/{self.employee.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
