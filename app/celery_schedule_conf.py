from celery.schedules import crontab

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

CELERY_BEAT_SCHEDULE = {
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

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
