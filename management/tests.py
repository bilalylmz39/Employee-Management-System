from django.test import TestCase
from django.contrib.auth.models import User
from management.models import Employee, Leave, Notification


class EmployeeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='password'
        )
        self.employee = Employee.objects.create(
            name="Test Employee",
            email="test@example.com",
            position="Developer"
        )

    def test_employee_creation(self):
        self.assertEqual(self.employee.name, "Test Employee")
        self.assertEqual(self.employee.email, "test@example.com")


class LeaveTests(TestCase):
    def setUp(self):
        self.employee = Employee.objects.create(
            name="Test Employee",
            email="test@example.com",
            position="Developer"
        )
        self.leave = Leave.objects.create(
            employee=self.employee,
            start_date="2024-11-01",
            end_date="2024-11-05"
        )

    def test_leave_creation(self):
        self.assertEqual(self.leave.days_requested, 5)
        self.assertEqual(self.leave.status, 'pending')


class NotificationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='admin', password='password', is_staff=True)
        self.notification = Notification.objects.create(
            recipient=self.user,
            notification_type='delay',
            message="Test notification"
        )

    def test_notification_creation(self):
        self.assertEqual(self.notification.recipient.username, 'admin')
        self.assertEqual(self.notification.notification_type, 'delay')
        self.assertFalse(self.notification.is_read)
