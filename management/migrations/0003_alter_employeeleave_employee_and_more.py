# Generated by Django 4.2.6 on 2024-11-23 23:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('management', '0002_employeeleave_workhours_delete_attendancerecord'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeleave',
            name='employee',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='leave',
            name='days_requested',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
