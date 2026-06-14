from rest_framework import viewsets, generics, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsAdmin, IsWorker
from django.db.models import Q
from .serializers import (
    TasksSerializer,
    TaskReaderSerializer,
    TaskWorkerSerializer,
    TaskAdminFullSerializer,
    TaskAdminSerializer,
)
from .filters import BaseTasksFilter, TaskWorkerFinishedFilter, TaskWorkerPendingFilter
from .models import Tasks

# =====================
# Reader Views
# =====================


class TaskReaderView(
    generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin
):
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
    permission_classes = [IsWorker]
    serializer_class = TaskWorkerSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BaseTasksFilter
    search_fields = ["title", "task_functor__username", "owner__username"]
    ordering_fields = ["created_date", "dead_line"]
    ordering = "-dead_line"

    def get_queryset(self):
        return Tasks.objects.filter(task_functor=self.request.user).exclude(
            status__in=["finished", "pending"]
        )

    def get(self, request, *args, **kwargs):

        return self.list(request, *args, **kwargs)


class TaskWorkerDetailViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
):
    permission_classes = [IsWorker]
    queryset = Tasks.objects.all()
    serializer_class = TaskWorkerSerializer
    lookup_field = "pk"

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.status != Tasks.TaskStatus.PENDING:
            instance.status = Tasks.TaskStatus.PENDING
            instance.save(update_fields=["status"])


class TaskWorkerFinishedViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = [IsWorker]
    serializer_class = TaskReaderSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = TaskWorkerFinishedFilter
    search_fields = ["title", "task_functor__username", "owner__username"]
    ordering_fields = ["created_date", "dead_line"]
    ordering = "-dead_line"

    def get_queryset(self):
        return Tasks.objects.filter(status="finished", task_functor=self.request.user)


class TaskWorkerPendingViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = [IsWorker]
    serializer_class = TaskReaderSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = TaskWorkerPendingFilter
    search_fields = ["title", "task_functor__username", "owner__username"]
    ordering_fields = ["created_date", "dead_line"]
    ordering = "-dead_line"

    def get_queryset(self):
        return Tasks.objects.filter(status="pending", task_functor=self.request.user)


# =====================
# Admin Views
# =====================
class TaskAdminFullViewSet(viewsets.ModelViewSet):
    queryset = Tasks.objects.all()
    serializer_class = TaskAdminFullSerializer
    permission_classes = [IsAdmin]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_class = BaseTasksFilter
    search_fields = ["title", "task_functor__username", "owner__username"]
    ordering_fields = ["created_date", "dead_line"]
    ordering = "-dead_line"

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskAdminListViewSet(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = Tasks.objects.filter(status="pending")
    serializer_class = TaskAdminSerializer
    permission_classes = [IsAdmin]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_class = BaseTasksFilter
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
    permission_classes = [IsAdmin]
    queryset = queryset = Tasks.objects.filter(status="pending")
    lookup_field = "pk"
    serializer_class = TaskAdminSerializer
