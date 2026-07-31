from datetime import date, timedelta

import pytest
from rest_framework.test import APIClient

from taskmanager.models import Tasks


@pytest.fixture
def api_client():
    """Return an anonymous API client."""
    return APIClient()


@pytest.fixture
def admin_user(db, django_user_model):
    """Create an admin user."""
    return django_user_model.objects.create_user(
        username="admin_user",
        email="admin@example.com",
        password="test-password-123",
        role="admin",
    )


@pytest.fixture
def worker_user(db, django_user_model):
    """Create a worker user."""
    return django_user_model.objects.create_user(
        username="worker_user",
        email="worker@example.com",
        password="test-password-123",
        role="worker",
    )


@pytest.fixture
def second_worker(db, django_user_model):
    """Create another worker user."""
    return django_user_model.objects.create_user(
        username="second_worker",
        email="second-worker@example.com",
        password="test-password-123",
        role="worker",
    )


@pytest.fixture
def reader_user(db, django_user_model):
    """Create a reader user."""
    return django_user_model.objects.create_user(
        username="reader_user",
        email="reader@example.com",
        password="test-password-123",
        role="reader",
    )


@pytest.fixture
def admin_client(admin_user):
    """Return an authenticated admin API client."""
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client


@pytest.fixture
def worker_client(worker_user):
    """Return an authenticated worker API client."""
    client = APIClient()
    client.force_authenticate(user=worker_user)
    return client


@pytest.fixture
def second_worker_client(second_worker):
    """Return an authenticated second worker API client."""
    client = APIClient()
    client.force_authenticate(user=second_worker)
    return client


@pytest.fixture
def reader_client(reader_user):
    """Return an authenticated reader API client."""
    client = APIClient()
    client.force_authenticate(user=reader_user)
    return client


@pytest.fixture
def task_factory(db, admin_user, worker_user):
    """Create tasks with customizable fields."""

    def create_task(**kwargs):
        task_data = {
            "owner": admin_user,
            "title": "Test task",
            "task": "Complete the assigned task.",
            "task_functor": worker_user,
            "dead_line": date.today() + timedelta(days=7),
            "status": Tasks.TaskStatus.DRAFT,
        }

        task_data.update(kwargs)

        return Tasks.objects.create(**task_data)

    return create_task
