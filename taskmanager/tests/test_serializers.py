import pytest

from taskmanager.models import Tasks
from taskmanager.serializers import (
    AdminChangeRoleSerializer,
    TaskAdminSerializer,
    TaskWorkerSerializer,
)

pytestmark = pytest.mark.django_db


def test_worker_serializer_keeps_status_read_only(
    task_factory,
):
    task = task_factory(status=Tasks.TaskStatus.REJECTED)

    serializer = TaskWorkerSerializer(
        instance=task,
        data={
            "status": Tasks.TaskStatus.FINISHED,
            "worker_massage": "Task completed.",
        },
        partial=True,
    )

    assert serializer.is_valid(), serializer.errors
    assert "status" not in serializer.validated_data
    assert serializer.validated_data["worker_massage"] == "Task completed."


def test_admin_waiting_serializer_allows_status_update(
    task_factory,
):
    task = task_factory(status=Tasks.TaskStatus.PENDING)

    serializer = TaskAdminSerializer(
        instance=task,
        data={
            "title": "Changed title",
            "status": Tasks.TaskStatus.REJECTED,
            "rejection_reason": "More work is required.",
        },
        partial=True,
    )

    assert serializer.is_valid(), serializer.errors

    assert "title" not in serializer.validated_data
    assert serializer.validated_data["status"] == Tasks.TaskStatus.REJECTED
    assert serializer.validated_data["rejection_reason"] == "More work is required."


def test_change_role_serializer_only_updates_role(
    worker_user,
):
    serializer = AdminChangeRoleSerializer(
        instance=worker_user,
        data={
            "username": "changed_username",
            "role": "reader",
        },
        partial=True,
    )

    assert serializer.is_valid(), serializer.errors
    assert "username" not in serializer.validated_data
    assert serializer.validated_data["role"] == "reader"
