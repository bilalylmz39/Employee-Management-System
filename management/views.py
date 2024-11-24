from datetime import time, timezone
import datetime
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
    UpdateAPIView,
    CreateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from .models import Employee, Leave, Notification, WorkHours
from .serializers import (
    EmployeeSerializer,
    LeaveDetailSerializer,
    LeaveManagerCheckSerializer,
    LeaveSerializer,
    NotificationSerializer,
    WorkHoursSerializer,
)
from .permissions import IsAdminOrReadOnly


# EMPLOYEE MANAGEMENT
class CreateEmployeeView(ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminOrReadOnly]


class ManagerDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]


# LEAVE MANAGEMENT
class CreateEmployeeLeaveView(ListCreateAPIView):
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer
    permission_classes = [IsAuthenticated]


class EmployeeLeaveListView(ListAPIView):
    queryset = Leave.objects.all()
    serializer_class = LeaveDetailSerializer
    permission_classes = [IsAuthenticated]


class ManagerLeaveCheckView(RetrieveUpdateDestroyAPIView):
    queryset = Leave.objects.all()
    serializer_class = LeaveManagerCheckSerializer
    permission_classes = [IsAdminOrReadOnly]


# NOTIFICATION MANAGEMENT
class ClockInView(CreateAPIView):
    serializer_class = WorkHoursSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(
            employee=self.request.user.employee,
            clock_in=timezone.now()
        )


class ClockOutView(UpdateAPIView):
    queryset = WorkHours.objects.all()
    serializer_class = WorkHoursSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        instance = self.get_object()
        clock_out_time = timezone.now()
        delay = None

        if instance.clock_in.time() > time(8, 0):
            delay = instance.clock_in - datetime.combine(
                instance.date,
                time(8, 0)
            )

        serializer.save(
            clock_out=clock_out_time,
            delay=delay
        )


class NotificationListView(ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)
