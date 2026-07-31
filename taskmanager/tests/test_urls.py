from django.urls import resolve, reverse
from django.test import SimpleTestCase

from taskmanager.views import (
    AdminChangeRoleViewSet,
    TaskAdminDetailsViewSet,
    TaskAdminFullViewSet,
    TaskAdminListViewSet,
    TaskReaderView,
    TaskWorkerDetailViewSet,
    TaskWorkerFinishedViewSet,
    TaskWorkerListView,
    TaskWorkerPendingViewSet,
)


class TaskURLTests(SimpleTestCase):

    def test_reader_list_url_resolves(self):
        url = reverse("tasks-reader-list")

        assert resolve(url).func.view_class is TaskReaderView

    def test_reader_detail_url_resolves(self):
        url = reverse(
            "task-reader-deatails",
            kwargs={"pk": 1},
        )

        assert resolve(url).func.view_class is TaskReaderView

    def test_worker_list_url_resolves(self):
        url = reverse("task-worker-list")

        assert resolve(url).func.view_class is TaskWorkerListView

    def test_worker_detail_url_resolves(self):
        url = reverse(
            "task-worker-details",
            kwargs={"pk": 1},
        )

        assert resolve(url).func.cls is TaskWorkerDetailViewSet

    def test_worker_pending_url_resolves(self):
        url = reverse("task-worker-pending")

        assert resolve(url).func.cls is TaskWorkerPendingViewSet

    def test_worker_finished_url_resolves(self):
        url = reverse("task-worker-finished")

        assert resolve(url).func.cls is TaskWorkerFinishedViewSet

    def test_admin_waiting_list_url_resolves(self):
        url = reverse("task-admin-list")

        assert resolve(url).func.view_class is TaskAdminListViewSet

    def test_admin_waiting_detail_url_resolves(self):
        url = reverse(
            "task-admin-waiting-details",
            kwargs={"pk": 1},
        )

        assert resolve(url).func.cls is TaskAdminDetailsViewSet

    def test_admin_full_router_url_resolves(self):
        url = reverse("tasks-admin-list")

        assert resolve(url).func.cls is TaskAdminFullViewSet

    def test_change_role_router_url_resolves(self):
        url = reverse("change-user-roles-list")

        assert resolve(url).func.cls is AdminChangeRoleViewSet
