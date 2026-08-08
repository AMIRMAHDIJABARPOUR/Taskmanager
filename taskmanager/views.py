# =====================
# Import
# =====================
#  restframework
from rest_framework import viewsets, generics, mixins
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter

# thirdpart import
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model

# local import
from .permissions import IsAdmin, IsWorker
from .serializers import (
    TaskReaderSerializer,
    TaskWorkerSerializer,
    TaskAdminFullSerializer,
    TaskAdminSerializer,
    AdminChangeRoleSerializer,
)
from .filters import BaseTasksFilter, TaskFilterWithoutStatus
from .models import Tasks
from .pagination import TaskPagination

User = get_user_model()
# =====================
# Reader Views
# =====================


class TaskReaderView(
    generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin
):
    pagination_class = TaskPagination
    queryset = Tasks.objects.all()
    serializer_class = TaskReaderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = BaseTasksFilter
    search_fields = ["title", "owner__username", "task_functor__username"]
    ordering_fields = ["created_date", "dead_line"]
    ordering = "-dead_line"

    def get(self, request, *args, **kwargs):
        if "pk" in kwargs:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)


# =====================
# Worker Views
# =====================


class TaskWorkerListView(
    generics.GenericAPIView,
    mixins.ListModelMixin,
):
    permission_classes = [IsAuthenticated, IsWorker]
    serializer_class = TaskWorkerSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BaseTasksFilter
    search_fields = ["title", "task_functor__username", "owner__username"]
    ordering_fields = ["created_date", "dead_line"]
    ordering = "-dead_line"
    pagination_class = TaskPagination

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Tasks.objects.none()

        return Tasks.objects.filter(task_functor=self.request.user).exclude(
            status__in=["finished", "pending"]
        )

    def get(self, request, *args, **kwargs):

        return self.list(request, *args, **kwargs)


class TaskWorkerDetailViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsWorker]
    queryset = Tasks.objects.all()
    serializer_class = TaskWorkerSerializer
    lookup_field = "pk"

    def get_queryset(self):
        return Tasks.objects.filter(task_functor=self.request.user)

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.status != Tasks.TaskStatus.PENDING:
            instance.status = Tasks.TaskStatus.PENDING
            instance.save(update_fields=["status"])


class TaskWorkerFinishedViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):

    permission_classes = [IsAuthenticated, IsWorker]
    pagination_class = TaskPagination
    serializer_class = TaskReaderSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = TaskFilterWithoutStatus
    search_fields = ["title", "task_functor__username", "owner__username"]
    ordering_fields = ["created_date", "dead_line"]
    ordering = "-dead_line"

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Tasks.objects.none()

        return Tasks.objects.filter(
            status="finished",
            task_functor=self.request.user,
        )


class TaskWorkerPendingViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):

    permission_classes = [IsAuthenticated, IsWorker]
    pagination_class = TaskPagination
    serializer_class = TaskReaderSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = TaskFilterWithoutStatus
    search_fields = ["title", "task_functor__username", "owner__username"]
    ordering_fields = ["created_date", "dead_line"]
    ordering = "-dead_line"

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Tasks.objects.none()

        return Tasks.objects.filter(
            status="pending",
            task_functor=self.request.user,
        )


# =====================
# Admin Views
# =====================
class TaskAdminFullViewSet(viewsets.ModelViewSet):
    queryset = Tasks.objects.all()
    serializer_class = TaskAdminFullSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = TaskPagination
    filterset_class = BaseTasksFilter
    search_fields = ["title", "task_functor__username", "owner__username"]
    ordering_fields = ["created_date", "dead_line"]
    ordering = "-dead_line"

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskAdminListViewSet(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = Tasks.objects.filter(status="pending")
    serializer_class = TaskAdminSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BaseTasksFilter
    pagination_class = TaskPagination

    search_fields = ["title", "task_functor__username", "owner__username"]
    ordering_fields = ["created_date", "dead_line"]
    ordering = "-dead_line"

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskAdminDetailsViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
):
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = Tasks.objects.filter(status="pending")
    lookup_field = "pk"
    serializer_class = TaskAdminSerializer


class AdminChangeRoleViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminChangeRoleSerializer
    pagination_class = TaskPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    permission_classes = [IsAuthenticated, IsAdmin]
    http_method_names = ["get", "patch", "head", "options"]
