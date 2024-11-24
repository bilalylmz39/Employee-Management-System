from celery.schedules import crontab
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

CELERYBEAT_SCHEDULE = {
    'check-employee-delays': {
        'task': 'your_app.tasks.check_employee_delays',
        'schedule': crontab(hour=9),  # Run at 9 AM daily
    },
    'check-leave-balance': {
        'task': 'your_app.tasks.check_leave_balance',
        'schedule': crontab(0, 0, day_of_month='1'),  # Run monthly
    },
    'generate-monthly-report': {
        'task': 'your_app.tasks.generate_monthly_report',
        'schedule': crontab(0, 0, day_of_month='1'),  # Run monthly
    },
}
