from celery import shared_task
from datetime import time, timedelta
from django.utils import timezone
from django.db.models import Sum

from management.models import (
    EmployeeLeaveInfo, Notification, WorkHours, Employee
)
from django.contrib.auth.models import User


@shared_task
def check_employee_delays():
    today = timezone.now().date()
    start_time = time(8, 0)  # 08:00

    work_hours = WorkHours.objects.filter(
        date=today,
        clock_in__time__gt=start_time
    )

    for wh in work_hours:
        delay = wh.clock_in.time() - start_time
        if delay.total_seconds() > 0:
            # Update employee's leave balance
            leave_info = EmployeeLeaveInfo.objects.get(employee=wh.employee)
            leave_info.total_delay += delay

            # If delay is more than 8 hours (1 work day), deduct a leave day
            if leave_info.total_delay.total_seconds() >= 28800:
                leave_info.remaining_leave -= 1
                leave_info.total_delay = timedelta()

            leave_info.save()

            # Create notification for admin
            Notification.objects.create(
                recipient=User.objects.filter(is_staff=True).first(),
                notification_type='delay',
                message=(
                    f"Employee {wh.employee.name} was "
                    f"{delay.total_seconds()/60:.0f} minutes late today"
                )
            )


@shared_task
def check_leave_balance():
    employees = EmployeeLeaveInfo.objects.filter(remaining_leave__lt=3)

    for emp in employees:
        Notification.objects.create(
            recipient=User.objects.filter(is_staff=True).first(),
            notification_type='leave',
            message=(
                f"Employee {emp.employee.name} has less than 3 days of "
                "leave remaining"
            )
        )


@shared_task
def generate_monthly_report():
    last_month = timezone.now().replace(day=1) - timedelta(days=1)
    work_hours = WorkHours.objects.filter(
        date__year=last_month.year,
        date__month=last_month.month
    )

    for employee in Employee.objects.all():
        emp_hours = work_hours.filter(employee=employee).aggregate(
            total_hours=Sum('clock_out') - Sum('clock_in')
        )
        # Use emp_hours to create a report or log the total hours
        Notification.objects.create(
            recipient=User.objects.filter(is_staff=True).first(),
            notification_type='report',
            message=(
                f"Employee {employee.name} worked "
                f"{emp_hours['total_hours']} hours last month"
            )
        )
