import pytest
from django.urls import reverse
from rest_framework import status

from taskmanager.models import Tasks

pytestmark = pytest.mark.django_db


def get_response_items(response):
    """Return paginated or non-paginated response items."""
    if isinstance(response.data, dict) and "results" in response.data:
        return response.data["results"]

    return response.data


def test_reader_list_returns_all_tasks(
    reader_client,
    task_factory,
):
    first_task = task_factory(title="First task")

    second_task = task_factory(title="Second task")

    response = reader_client.get(reverse("tasks-reader-list"))

    assert response.status_code == status.HTTP_200_OK

    items = get_response_items(response)
    returned_ids = {item["id"] for item in items}

    assert first_task.pk in returned_ids
    assert second_task.pk in returned_ids

    assert all("task_url" in item for item in items)


def test_reader_detail_returns_selected_task(
    reader_client,
    task_factory,
):
    task = task_factory(title="Reader detail task")

    response = reader_client.get(
        reverse(
            "task-reader-deatails",
            kwargs={"pk": task.pk},
        )
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == task.pk
    assert response.data["title"] == "Reader detail task"
    assert "task_url" not in response.data


def test_reader_search_returns_matching_task(
    reader_client,
    task_factory,
):
    matching_task = task_factory(title="Django API testing")

    task_factory(title="Python command line")

    response = reader_client.get(
        reverse("tasks-reader-list"),
        {"search": "Django"},
    )

    assert response.status_code == status.HTTP_200_OK

    items = get_response_items(response)

    assert len(items) == 1
    assert items[0]["id"] == matching_task.pk


def test_worker_list_returns_only_own_active_tasks(
    worker_client,
    worker_user,
    second_worker,
    task_factory,
):
    draft_task = task_factory(
        task_functor=worker_user,
        status=Tasks.TaskStatus.DRAFT,
    )

    rejected_task = task_factory(
        task_functor=worker_user,
        status=Tasks.TaskStatus.REJECTED,
    )

    task_factory(
        task_functor=worker_user,
        status=Tasks.TaskStatus.PENDING,
    )

    task_factory(
        task_functor=worker_user,
        status=Tasks.TaskStatus.FINISHED,
    )

    task_factory(
        task_functor=second_worker,
        status=Tasks.TaskStatus.DRAFT,
    )

    response = worker_client.get(reverse("task-worker-list"))

    assert response.status_code == status.HTTP_200_OK

    items = get_response_items(response)

    returned_ids = {item["id"] for item in items}

    assert returned_ids == {
        draft_task.pk,
        rejected_task.pk,
    }


def test_worker_can_retrieve_own_task(
    worker_client,
    worker_user,
    task_factory,
):
    task = task_factory(task_functor=worker_user)

    response = worker_client.get(
        reverse(
            "task-worker-details",
            kwargs={"pk": task.pk},
        )
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == task.pk


def test_worker_cannot_retrieve_another_worker_task(
    worker_client,
    second_worker,
    task_factory,
):
    task = task_factory(task_functor=second_worker)

    response = worker_client.get(
        reverse(
            "task-worker-details",
            kwargs={"pk": task.pk},
        )
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_worker_update_changes_status_to_pending(
    worker_client,
    worker_user,
    task_factory,
):
    task = task_factory(
        task_functor=worker_user,
        status=Tasks.TaskStatus.REJECTED,
    )

    response = worker_client.patch(
        reverse(
            "task-worker-details",
            kwargs={"pk": task.pk},
        ),
        {
            "worker_massage": "The task is complete.",
        },
        format="multipart",
    )

    assert response.status_code == status.HTTP_200_OK

    task.refresh_from_db()

    assert task.worker_massage == "The task is complete."
    assert task.status == Tasks.TaskStatus.PENDING


def test_worker_pending_list_returns_only_own_pending_tasks(
    worker_client,
    worker_user,
    second_worker,
    task_factory,
):
    own_pending_task = task_factory(
        task_functor=worker_user,
        status=Tasks.TaskStatus.PENDING,
    )

    task_factory(
        task_functor=second_worker,
        status=Tasks.TaskStatus.PENDING,
    )

    task_factory(
        task_functor=worker_user,
        status=Tasks.TaskStatus.DRAFT,
    )

    response = worker_client.get(reverse("task-worker-pending"))

    assert response.status_code == status.HTTP_200_OK

    items = get_response_items(response)

    assert {item["id"] for item in items} == {own_pending_task.pk}


def test_worker_finished_list_returns_only_own_finished_tasks(
    worker_client,
    worker_user,
    second_worker,
    task_factory,
):
    own_finished_task = task_factory(
        task_functor=worker_user,
        status=Tasks.TaskStatus.FINISHED,
    )

    task_factory(
        task_functor=second_worker,
        status=Tasks.TaskStatus.FINISHED,
    )

    task_factory(
        task_functor=worker_user,
        status=Tasks.TaskStatus.PENDING,
    )

    response = worker_client.get(reverse("task-worker-finished"))

    assert response.status_code == status.HTTP_200_OK

    items = get_response_items(response)

    assert {item["id"] for item in items} == {own_finished_task.pk}


def test_admin_can_create_task_and_becomes_owner(
    admin_client,
    admin_user,
    worker_user,
):
    response = admin_client.post(
        reverse("tasks-admin-list"),
        {
            "title": "Task created by admin",
            "task": "Implement the requested feature.",
            "task_functor": worker_user.pk,
            "dead_line": "2030-12-30",
            "status": Tasks.TaskStatus.DRAFT,
        },
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED

    created_task = Tasks.objects.get(title="Task created by admin")

    assert created_task.owner == admin_user
    assert created_task.task_functor == worker_user


def test_admin_waiting_list_returns_only_pending_tasks(
    admin_client,
    task_factory,
):
    pending_task = task_factory(status=Tasks.TaskStatus.PENDING)

    task_factory(status=Tasks.TaskStatus.DRAFT)

    task_factory(status=Tasks.TaskStatus.FINISHED)

    response = admin_client.get(reverse("task-admin-list"))

    assert response.status_code == status.HTTP_200_OK

    items = get_response_items(response)

    assert {item["id"] for item in items} == {pending_task.pk}


def test_admin_can_reject_pending_task(
    admin_client,
    task_factory,
):
    task = task_factory(status=Tasks.TaskStatus.PENDING)

    response = admin_client.patch(
        reverse(
            "task-admin-waiting-details",
            kwargs={"pk": task.pk},
        ),
        {
            "status": Tasks.TaskStatus.REJECTED,
            "rejection_reason": "The submitted result is incomplete.",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK

    task.refresh_from_db()

    assert task.status == Tasks.TaskStatus.REJECTED
    assert task.rejection_reason == "The submitted result is incomplete."


def test_admin_can_delete_task_from_full_endpoint(
    admin_client,
    task_factory,
):
    task = task_factory()
    task_id = task.pk

    response = admin_client.delete(
        reverse(
            "tasks-admin-detail",
            kwargs={"pk": task.pk},
        )
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Tasks.objects.filter(pk=task_id).exists() is False


def test_admin_can_change_user_role(
    admin_client,
    worker_user,
):
    response = admin_client.patch(
        reverse(
            "change-user-roles-detail",
            kwargs={"pk": worker_user.pk},
        ),
        {
            "role": "reader",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK

    worker_user.refresh_from_db()

    assert worker_user.role == "reader"
