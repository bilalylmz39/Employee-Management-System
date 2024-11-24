from rest_framework import serializers
from .models import Employee, Leave
from django.contrib.auth import authenticate


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            username=data['username'], password=data['password']
        )
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Geçersiz kullanıcı adı veya şifre.")


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name', 'email', 'position', 'date_joined']


class ManagerLeaveSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)

    class Meta:
        model = Leave
        fields = '__all__'


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
