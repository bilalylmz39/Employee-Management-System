from celery import Celery
from celery.schedules import crontab

app = Celery('app')

app.conf.beat_schedule = {
    'check-leave-balance-daily': {
        'task': 'leave.tasks.check_leave_balance',
        'schedule': crontab(hour=0, minute=0),
    },
}

app.conf.beat_schedule = {
    'check-annual-leave-daily': {
        'task': 'attendance.tasks.check_annual_leave',
        'schedule': crontab(hour=0, minute=0),
    },
}
