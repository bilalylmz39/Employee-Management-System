import datetime
from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    position = models.CharField(max_length=100)
    date_joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class EmployeeLeaveInfo(models.Model):
    employee = models.OneToOneField(User, on_delete=models.CASCADE)
    leave_balance = models.IntegerField(default=15)  # Automatic 15 days leave
    total_delay = models.DurationField(default=datetime.timedelta)
    annual_leave = models.IntegerField(default=15)  # Annual leave days
    remaining_leave = models.IntegerField(default=0)  # Remaining leave days

    def __str__(self):
        return self.user.username


class WorkHours(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.datetime.now)
    clock_in = models.DateTimeField()
    clock_out = models.DateTimeField()
    delay = models.DurationField(null=True, blank=True)

    def __str__(self):
        return f"{self.employee.user.username} - {self.date}"


class Leave(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="leaves"
    )
    start_date = models.DateField()
    end_date = models.DateField()
    days_requested = models.IntegerField(null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.name} - {self.start_date} to {self.end_date}"
