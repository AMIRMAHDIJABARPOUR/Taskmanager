import django_filters
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Tasks


class BaseTasksFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
    created_before = django_filters.DateFilter(
        field_name="created_date", lookup_expr="lte"
    )
    created_after = django_filters.DateFilter(
        field_name="created_date", lookup_expr="gte"
    )
    deadline_before = django_filters.DateFilter(
        field_name="dead_line", lookup_expr="lte"
    )
    deadline_after = django_filters.DateFilter(
        field_name="dead_line", lookup_expr="gte"
    )
    status = django_filters.ChoiceFilter(
        field_name="status", choices=Tasks.TaskStatus.choices
    )
    rejection_reason = django_filters.BooleanFilter(
        field_name="rejection_reason", lookup_expr="isnull", exclude=True
    )

    class Meta:
        model = Tasks
        fields = []


class TaskWorkerFinishedFilter(BaseTasksFilter):
    status = None


class TaskWorkerPendingFilter(BaseTasksFilter):
    status = None
