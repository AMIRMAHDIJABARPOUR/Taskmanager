import pytest

from taskmanager.models import Tasks

pytestmark = pytest.mark.django_db


def test_task_default_status_is_draft(task_factory):
    task = task_factory()

    assert task.status == Tasks.TaskStatus.DRAFT


def test_task_string_representation(task_factory):
    task = task_factory(
        title="Complete API tests",
        status=Tasks.TaskStatus.PENDING,
    )

    assert str(task) == "Complete API tests (pending)"


def test_deleting_owner_deletes_owned_task(
    admin_user,
    task_factory,
):
    task = task_factory(owner=admin_user)
    task_id = task.pk

    admin_user.delete()

    assert Tasks.objects.filter(pk=task_id).exists() is False
