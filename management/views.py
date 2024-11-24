from datetime import time, timezone
import datetime
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
    UpdateAPIView,
    CreateAPIView,
)
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from .models import (
    Employee,
    EmployeeDashboard,
    Leave,
    Notification,
    WorkHours,
    ManagerDashboard
)
from django.shortcuts import redirect, render
from .serializers import (
    EmployeeSerializer,
    LeaveDetailSerializer,
    LeaveManagerCheckSerializer,
    LeaveSerializer,
    NotificationSerializer,
    WorkHoursSerializer,
)
from .permissions import IsAdminOrReadOnly


# AUTH
class LoginView(APIView):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            # Kullanıcı türüne göre yönlendirme yapabiliriz
            if user.is_staff:
                return redirect('manager_dashboard')
            else:
                return redirect('employee_dashboard')
        else:
            return Response(
                {'detail': 'Invalid credentials'},
                status=status.HTTP_400_BAD_REQUEST
            )


class LogoutView(APIView):
    def get(self, request):
        return render(request, 'logout.html')

    def post(self, request):
        logout(request)
        return redirect('login')


class ManagerDashboardView(APIView):
    def get(self, request):
        dashboard = ManagerDashboard.objects.get_or_create(
            user=request.user
        )
        employees = Employee.objects.all()
        leave_requests = Leave.objects.all()
        return render(
            request,
            'manager_dashboard.html',
            {
                'dashboard': dashboard,
                'employees': employees,
                'leave_requests': leave_requests
            }
        )


class EmployeeDashboardView(APIView):
    def get(self, request):
        dashboard = EmployeeDashboard.objects.get_or_create(
            user=request.user
        )
        leave_requests = Leave.objects.all()
        return render(
            request,
            'employee_dashboard.html',
            {'dashboard': dashboard, 'leave_requests': leave_requests}
        )


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


class EmployeeLeaveListView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'employee_leaves.html'

    def get(self, request):
        leave_requests = Leave.objects.all()
        leave_data = LeaveDetailSerializer(leave_requests, many=True)
        return Response({'leave_requests': leave_data.data})


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
