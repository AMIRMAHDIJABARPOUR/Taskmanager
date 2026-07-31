import pytest
from django.urls import reverse
from rest_framework import status

pytestmark = pytest.mark.django_db


def test_anonymous_user_cannot_access_reader_list(
    api_client,
):
    response = api_client.get(reverse("tasks-reader-list"))

    assert response.status_code in {
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_403_FORBIDDEN,
    }


def test_reader_cannot_access_worker_list(
    reader_client,
):
    response = reader_client.get(reverse("task-worker-list"))

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_worker_can_access_worker_list(
    worker_client,
):
    response = worker_client.get(reverse("task-worker-list"))

    assert response.status_code == status.HTTP_200_OK


def test_reader_cannot_access_admin_tasks(
    reader_client,
):
    response = reader_client.get(reverse("tasks-admin-list"))

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_worker_cannot_access_admin_tasks(
    worker_client,
):
    response = worker_client.get(reverse("tasks-admin-list"))

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_admin_can_access_admin_tasks(
    admin_client,
):
    response = admin_client.get(reverse("tasks-admin-list"))

    assert response.status_code == status.HTTP_200_OK
