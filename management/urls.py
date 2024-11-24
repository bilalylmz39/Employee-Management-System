from django.urls import path
from . import views as api_views


urlpatterns = [
    # Manager
    path('manager/<int:pk>/', api_views.ManagerDetailView.as_view()),
    # path('manager/report/', api_views.EmployeeReportView.as_view()),
    path('manager/', api_views.CreateEmployeeView.as_view()),
    path('manager/leave/<int:pk>/', api_views.ManagerLeaveCheckView.as_view()),
    path('manager/leaves/', api_views.EmployeeLeaveListView.as_view()),
    # path('manager/login/', api_views.LoginView.as_view(), name='login'),
    # path('manager/logout/', api_views.LogoutView.as_view(), name='logout'),s
    # Employee
    path('employee/leave/', api_views.CreateEmployeeLeaveView.as_view()),
    # path('employee/logout/', api_views.LogoutView.as_view(), name='logout'),
]
