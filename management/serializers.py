from rest_framework import serializers
from .models import Employee, Leave, Notification, WorkHours


# EMPLOYEE MANAGEMENT
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name', 'email', 'position', 'date_joined']


# LEAVE MANAGEMENT
class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = [
            'id', 'employee', 'start_date', 'end_date',
            'status', 'created_at'
        ]
        read_only_fields = ['status', 'created_at']


class LeaveDetailSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)

    class Meta:
        model = Leave
        fields = '__all__'


class LeaveManagerCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = '__all__'
        read_only_fields = [
            'start_date', 'end_date', 'days_requested', 'employee'
        ]


class ManagerLeaveSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)

    class Meta:
        model = Leave
        fields = '__all__'


# NOTIFICATION MANAGEMENT
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class WorkHoursSerializer(serializers.ModelSerializer):
    delay_minutes = serializers.SerializerMethodField()

    class Meta:
        model = WorkHours
        fields = [
            'id', 'employee', 'date', 'clock_in', 'clock_out', 'delay',
            'delay_minutes'
        ]

    def get_delay_minutes(self, obj):
        if obj.delay:
            return obj.delay.total_seconds() / 60
        return 0
