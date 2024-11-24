from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout
from .models import Employee, Leave
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import (
    EmployeeSerializer,
    LeaveDetailSerializer,
    LeaveManagerCheckSerializer,
    LeaveSerializer,
    LoginSerializer
)
from .permissions import IsAdminOrReadOnly


class CreateEmployeeView(ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminOrReadOnly]


class ManagerDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response(
            {"message": "Başarıyla çıkış yapıldı."}, status=status.HTTP_200_OK
        )


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
