from django.urls import path

from management.consumer import NotificationConsumer
from . import views as api_views


urlpatterns = [
    # AUTH
    path('login/', api_views.LoginView.as_view(), name='login'),
    path('logout/', api_views.LogoutView.as_view(), name='logout'),

    # MANAGER
    path(
        'manager/dashboard/',
        api_views.ManagerDashboardView.as_view(),
        name='manager_dashboard'
    ),
    path('manager/<int:pk>/', api_views.ManagerDetailView.as_view()),
    path(
        'manager/',
        api_views.CreateEmployeeView.as_view(),
        name='create_employee'
    ),
    path(
        'manager/leave/<int:pk>/',
        api_views.ManagerLeaveCheckView.as_view(),
        name='manager_leave_check'
    ),
    path('manager/leaves/', api_views.EmployeeLeaveListView.as_view()),

    # EMPLOYEE
    path(
            'employee/dashboard/',
            api_views.EmployeeDashboardView.as_view(),
            name='employee_dashboard'
    ),
    path(
        'employee/leave/',
        api_views.CreateEmployeeLeaveView.as_view(),
        name='leave_request'
    ),

    # NOTIFICATION
    path('notification/clock-in/', api_views.ClockInView.as_view()),
    path('notification/clock-out/<int:pk>/', api_views.ClockOutView.as_view()),
    path('notifications/', api_views.NotificationListView.as_view()),

]

# WEBSOCKET
websocket_urlpatterns = [
    path('ws/notifications/', NotificationConsumer.as_asgi()),
]
