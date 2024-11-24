# Employee Attendance Tracking Application

## Setup
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Start Celery: `celery -A app worker -l info --beat`
5. Start the server: `python manage.py runserver`

## Authentication
1. Obtain a JWT token by providing valid credentials.
2. Use the /api/users/login/ endpoint to authenticate and obtain a JWT token.
3. Authorization: Bearer your_jwt_token

# Employee Attendance and Leave Management System

## Overview
This Django-based application allows companies to:
- Track employee attendance (entry/exit times).
- Manage annual leave balances.
- Notify admins for delays and low leave balances.
- Generate monthly working hour reports.

## Features
1. **Attendance Management**: Log daily entry/exit times and calculate delays.
2. **Leave Management**:
   - Auto-assign 15 leave days to new employees.
   - Employees can request leaves.
   - Admins can approve/reject leave requests.
   - Automatic deduction of leave days for late entries.
   - Notify admins when leave balance drops below 3 days.
3. **Notifications**: WebSocket-based real-time notifications.
4. **Monthly Reports**: Summarize employee work hours.


## Manager Endpoints
List all employees or create a new employee
`URL: /manager/`
Method: GET, POST

Retrieve, update, or delete a specific employee
`URL: /manager/<int:pk>/`
Method: GET, PUT, PATCH, DELETE

Review a specific leave request
`URL: /manager/leave/<int:pk>/`
Method: GET, PUT, DELETE

List all leave requests of employees
`URL: /manager/leaves/`
Method: GET

## Employee Endpoints
Create a new leave request
`URL: /employee/leave/`
Method: POST
Notification Endpoints
Clock in for work
`URL: /notification/clock-in/`
Method: POST

Clock out of work
`URL: /notification/clock-out/<int:pk>/`
Method: PUT

List all notifications for the user
`URL: /notifications/`
Method: GET

## WebSocket
Receive real-time notifications
`URL: /ws/notifications/`
Protocol: WebSocket