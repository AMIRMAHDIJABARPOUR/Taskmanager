# Task Manager API

A role-based task management REST API built with Django and Django REST Framework.  
The project is designed around a simple workflow where admins create and assign tasks, workers submit their work, and admins review submitted tasks.

## Overview

Task Manager API provides authentication, user role management, task assignment, worker submission, admin review, filtering, search, pagination, and interactive API documentation.

The main goal of this project is to practice backend API development with Django REST Framework and build a portfolio-ready API project with real-world permission and workflow logic.

## Features

- Custom user authentication with JWT
- Login with username or email
- Role-based access control
- Three user roles:
  - Admin
  - Worker
  - Reader
- Admin task management
- Worker task submission
- Reader read-only task access
- Admin review workflow for submitted tasks
- Task status workflow:
  - Draft
  - Pending
  - Rejected
  - Finished
- User role management by admin
- Image upload for worker task submission
- Filtering, search, ordering, and pagination
- Swagger and ReDoc API documentation
- Postman Collection for API testing

## Tech Stack

- Python
- Django
- Django REST Framework
- Djoser
- Simple JWT
- drf-spectacular
- django-filter
- Pillow
- Postman
- Swagger / ReDoc

## User Roles

| Role   | Access                                                                       |
| ------ | ---------------------------------------------------------------------------- |
| Admin  | Can create, update, delete, assign, and review tasks. Can manage user roles. |
| Worker | Can view assigned tasks and submit task results.                             |
| Reader | Can view tasks in read-only mode.                                            |

## Task Workflow

```text
Admin creates a task
        ↓
Admin assigns the task to a worker
        ↓
Worker submits task result
        ↓
Task status becomes pending
        ↓
Admin reviews the pending task
        ↓
Admin marks it as finished or rejected
```

## Main API Sections

### Authentication

| Method | Endpoint                             | Description                    |
| ------ | ------------------------------------ | ------------------------------ |
| POST   | `/accounts/auth/users/`              | Register a new user            |
| POST   | `/accounts/auth/jwt/create/`         | Login and receive JWT tokens   |
| POST   | `/accounts/auth/jwt/refresh/`        | Refresh access token           |
| POST   | `/accounts/auth/jwt/verify/`         | Verify JWT token               |
| POST   | `/accounts/auth/jwt/logout/`         | Blacklist refresh token        |
| GET    | `/accounts/auth/users/me/`           | Get current authenticated user |
| PATCH  | `/accounts/auth/users/me/`           | Update current user            |
| POST   | `/accounts/auth/users/set_password/` | Change password                |
| DELETE | `/accounts/auth/users/me/`           | Delete account                 |

### Reader Endpoints

| Method | Endpoint                         | Description                 |
| ------ | -------------------------------- | --------------------------- |
| GET    | `/taskmanager/tasks-reader/`     | Get read-only list of tasks |
| GET    | `/taskmanager/task-reader/<id>/` | Get task details            |

### Worker Endpoints

| Method | Endpoint                              | Description                                           |
| ------ | ------------------------------------- | ----------------------------------------------------- |
| GET    | `/taskmanager/tasks-worker/`          | Get active tasks assigned to the authenticated worker |
| GET    | `/taskmanager/task-worker/<id>/`      | Get details of a worker task                          |
| PATCH  | `/taskmanager/task-worker/<id>/`      | Submit worker task result                             |
| GET    | `/taskmanager/tasks-worker/pending/`  | Get submitted tasks waiting for admin review          |
| GET    | `/taskmanager/tasks-worker/finished/` | Get completed tasks assigned to the worker            |

### Admin Endpoints

| Method | Endpoint                                               | Description                          |
| ------ | ------------------------------------------------------ | ------------------------------------ |
| GET    | `/taskmanager/admin-full-page/tasks-admin/`            | Get all tasks                        |
| POST   | `/taskmanager/admin-full-page/tasks-admin/`            | Create a new task                    |
| GET    | `/taskmanager/admin-full-page/tasks-admin/<id>/`       | Get task details                     |
| PATCH  | `/taskmanager/admin-full-page/tasks-admin/<id>/`       | Partially update a task              |
| PUT    | `/taskmanager/admin-full-page/tasks-admin/<id>/`       | Fully update a task                  |
| DELETE | `/taskmanager/admin-full-page/tasks-admin/<id>/`       | Delete a task                        |
| GET    | `/taskmanager/admin-waiting-page/tasks-admin/`         | Get pending tasks waiting for review |
| GET    | `/taskmanager/admin-waiting-page/task-admin/<id>/`     | Get pending task details             |
| PATCH  | `/taskmanager/admin-waiting-page/task-admin/<id>/`     | Review a pending task                |
| GET    | `/taskmanager/admin-full-page/change-user-roles/`      | Get users for role management        |
| GET    | `/taskmanager/admin-full-page/change-user-roles/<id>/` | Get user role details                |
| PATCH  | `/taskmanager/admin-full-page/change-user-roles/<id>/` | Update user role                     |

## Filtering, Search, Ordering, and Pagination

The task list endpoints support filtering, search, ordering, and pagination.

Example query parameters:

```text
?title=login
?owner_username=admin
?task_functor_username=worker
?created_after=2026-07-01
?created_before=2026-07-30
?deadline_after=2026-07-01
?deadline_before=2026-07-30
?status=pending
?has_rejection_reason=true
?page=1
?page=1&page_size=5
?search=login
?ordering=-dead_line
```

## API Documentation

After running the project locally, API documentation is available at:

```text
Swagger UI:
http://127.0.0.1:8000/api/docs/swagger/

ReDoc:
http://127.0.0.1:8000/api/docs/redoc/

OpenAPI Schema:
http://127.0.0.1:8000/api/schema/
```

## Postman Collection

A Postman Collection is included for testing the API endpoints.  
The collection is organized into the following sections:

```text
Authenticator
├── Users
└── Auth

Manage Tasks
├── Reader
├── Worker
└── Admin
    ├── Full Management
    ├── Waiting Tasks
    └── User Management
```

Before sharing the collection publicly, remove all real tokens, passwords, emails, and test credentials.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/AMIRMAHDIJABARPOUR/Taskmanager
cd Taskmanager
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux / macOS:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a superuser

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

The project will be available at:

```text
http://127.0.0.1:8000/
```

## Environment Variables

Create a `.env` file for sensitive settings.

Example:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

Do not commit real secrets, production credentials, or JWT tokens to GitHub.

## Example Worker Task Submission

Workers can submit their task result using `PATCH` with form-data:

```text
worker_massage: Task result description
worker_task_image: uploaded image file
```

After submission, the task status is changed to `pending` and waits for admin review.

## Security Notes

- Protected endpoints require JWT authentication.
- Admin endpoints are restricted to admin users.
- Worker endpoints only return tasks assigned to the authenticated worker.
- Reader endpoints are read-only.
- User role changes are restricted to admin users.
- Real credentials and tokens should never be committed to GitHub.

## Project Structure

```text
project/
├── accounts/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── permissions.py
│
├── taskmanager/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── filters.py
│   ├── pagination.py
│   └── permissions.py
│
├── config/
│   ├── settings.py
│   └── urls.py
│
├── requirements.txt
└── README.md
```

## What I Learned

- Building REST APIs with Django REST Framework
- Implementing JWT authentication with Simple JWT
- Using Djoser for user account endpoints
- Designing role-based API permissions
- Working with ViewSets, GenericAPIView, serializers, and custom permissions
- Handling task workflows with multiple statuses
- Adding filtering, search, ordering, and pagination
- Documenting APIs with Swagger/OpenAPI
- Testing APIs with Postman

## Future Improvements

- Add automated tests for authentication, permissions, and task workflow.
- Add Docker support and deployment instructions.
- Add a notification system for task assignment and review results.
- Improve the Postman Collection by replacing test tokens with variables.

## Key Takeaways

- Built a role-based task management REST API using Django REST Framework.
- Implemented JWT authentication, custom user roles, and protected endpoints.
- Designed Admin, Worker, and Reader workflows with task submission and review logic.
- Added filtering, search, ordering, pagination, Swagger documentation, and Postman testing support.

## License

This project is for educational and portfolio purposes.
