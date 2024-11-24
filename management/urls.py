from django.urls import path
from . import views as api_views


urlpatterns = [

    # MANAGER
    path('manager/<int:pk>/', api_views.ManagerDetailView.as_view()),
    path('manager/', api_views.CreateEmployeeView.as_view()),
    path('manager/leave/<int:pk>/', api_views.ManagerLeaveCheckView.as_view()),
    path('manager/leaves/', api_views.EmployeeLeaveListView.as_view()),
    path('employee/clock-in/', api_views.ClockInView.as_view()),
    path('employee/clock-out/<int:pk>/', api_views.ClockOutView.as_view()),
    path('notifications/', api_views.NotificationListView.as_view()),


    # EMPLOYEE
    path('employee/leave/', api_views.CreateEmployeeLeaveView.as_view()),

]
