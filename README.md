# employee Attendance Tracking Application

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

### Example request:

`POST /api/users/login/`
Content-Type: application/json
{"username": "your_username", "password": "your_password"}
### Example response:
{"token": "your_jwt_token"}

## API Endpoints

### Authentication
Login: POST `/api/users/login/`
Authenticate the user and retrieve a JWT token.

Logout: POST `/api/users/logout/`
Log out the user and invalidate the JWT token.

### Employee Management
List employees: `GET /api/employees/`
Retrieve a list of all employees. (Requires Manager Access)

Create employee: `POST /api/employees/`
Add a new employee. (Requires Manager Access)

Retrieve employee Details: `GET /api/employees/<id>/`
View details of a specific employee.

Update employee Details: `PUT /api/employees/<id>/`
Update information for a specific employee. (Requires Manager Access)

Delete employee: `DELETE /api/employees/<id>/`
Remove an employee from the system. (Requires Manager Access)

### Attendance
Record Entry/Exit: `POST /api/attendance/`
Record an employee's entry or exit time.

View Attendance Logs: `GET /api/attendance/`
Retrieve the attendance logs for the authenticated user.

Manager Attendance Overview: `GET /api/attendance/overview/`
Get a summary of employee attendance, including late entries and total hours worked. (Requires Manager Access)

### Leave Management
Request Leave: `POST /api/leaves/request/`
Submit a leave request.

View Leave Requests: `GET /api/leaves/`
Retrieve the leave requests of the authenticated user.

Approve/Reject Leave: `POST /api/leaves/<id>/action/`
Approve or reject a leave request. (Requires Manager Access)

Manager Leave Overview: `GET /api/leaves/overview/`
View all leave records and their statuses. (Requires Manager Access)

## Notifications
### Celery Integration
Notifications for late arrivals and low annual leave balances are managed using Celery.

### WebSocket Integration
Real-time notifications are sent to the manager dashboard via WebSocket.

## Additional Notes
Ensure the RabbitMQ broker is running before starting Celery.
For API documentation, visit /swagger/ after starting the server.