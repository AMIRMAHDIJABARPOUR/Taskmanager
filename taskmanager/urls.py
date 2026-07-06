from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TaskReaderView,
    TaskWorkerListView,
    TaskWorkerDetailViewSet,
    TaskAdminFullViewSet,
    TaskAdminListViewSet,
    TaskAdminDetailsViewSet,
    TaskWorkerFinishedViewSet,
    TaskWorkerPendingViewSet,
    AdminChangeRoleViewSet,
)

router = DefaultRouter()
router.register(r"tasks-admin", TaskAdminFullViewSet, basename="tasks-admin")
router.register(
    r"change-user-roles", AdminChangeRoleViewSet, basename="change-user-roles"
)

urlpatterns = [
    # Reader Urls
    path("tasks-reader/", TaskReaderView.as_view(), name="tasks-reader-list"),
    path(
        "task-reader/<int:pk>/", TaskReaderView.as_view(), name="task-reader-deatails"
    ),
    # Worker Urls
    path("tasks-worker/", TaskWorkerListView.as_view(), name="task-worker-list"),
    path(
        "task-worker/<int:pk>/",
        TaskWorkerDetailViewSet.as_view(
            {
                "get": "retrieve",
                "patch": "partial_update",
            }
        ),
        name="task-worker-details",
    ),
    path(
        "tasks-worker/pending/",
        TaskWorkerPendingViewSet.as_view({"get": "list"}),
        name="task-worker-pending",
    ),
    path(
        "tasks-worker/finished/",
        TaskWorkerFinishedViewSet.as_view({"get": "list"}),
        name="task-worker-finished",
    ),
    # Admin Urls
    path("admin-full-page/", include(router.urls)),
    path(
        "admin-waiting-page/tasks-admin/",
        TaskAdminListViewSet.as_view(),
        name="task-admin-list",
    ),
    path(
        "admin-waiting-page/task-admin/<int:pk>/",
        TaskAdminDetailsViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
            }
        ),
        name="task-admin-waiting-details",
    ),
]
