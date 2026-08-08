from rest_framework import serializers
from rest_framework.reverse import reverse
from django.contrib.auth import get_user_model
from .models import Tasks

User = get_user_model()


# =====================
# Reader Serailizer
# =====================


class TaskReaderSerializer(serializers.ModelSerializer):
    owner_url = serializers.SerializerMethodField()
    owner_username = serializers.CharField(source="owner.username", read_only=True)
    task_functor_url = serializers.SerializerMethodField()
    task_functor_username = serializers.CharField(
        source="task_functor.username", read_only=True
    )
    task_url = serializers.SerializerMethodField()

    class Meta:
        model = Tasks

        fields = [
            "id",
            "task_url",
            "title",
            "task",
            "created_date",
            "dead_line",
            "owner",
            "owner_username",
            "owner_url",
            "task_functor",
            "task_functor_username",
            "task_functor_url",
            "status",
        ]

    def get_task_functor_url(self, obj) -> str:
        request = self.context.get("request")
        return reverse(
            "accounts-user-details",
            kwargs={"pk": obj.task_functor.pk},
            request=request,
        )

    def get_owner_url(self, obj) -> str:
        request = self.context.get("request")
        return reverse(
            "accounts-user-details", kwargs={"pk": obj.owner.pk}, request=request
        )

    def get_task_url(self, obj) -> str:
        request = self.context.get("request")
        return reverse("task-reader-deatails", kwargs={"pk": obj.pk}, request=request)

    def to_representation(self, instance) -> str:
        representation = super().to_representation(instance)
        view = self.context.get("view")
        action = getattr(view, "action", None)
        if action == "retrieve":
            representation.pop("task_url", None)
        return representation

    def get_fields(self) -> str:
        fields = super().get_fields()
        view = self.context.get("view")
        if hasattr(view, "kwargs") and view.kwargs.get("pk"):
            fields.pop("task_url", None)
        return fields


# =====================
# Worker Serializer
# =====================


class TaskWorkerSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source="owner.username", read_only=True)
    owner_url = serializers.SerializerMethodField()
    task_functor_username = serializers.CharField(
        source="task_functor.username", read_only=True
    )
    task_functor_url = serializers.SerializerMethodField()
    task_url = serializers.SerializerMethodField()

    class Meta:
        model = Tasks
        fields = [
            "id",
            "title",
            "task",
            "owner_username",
            "owner_url",
            "task_functor_username",
            "task_functor_url",
            "created_date",
            "dead_line",
            "status",
            "worker_massage",
            "worker_task_image",
            "rejection_reason",
            "task_url",
        ]

        read_only_fields = [
            "id",
            "task_url",
            "title",
            "task",
            "owner_username",
            "owner_url",
            "task_functor_username",
            "task_functor_url",
            "created_date",
            "dead_line",
            "rejection_reason",
            "status",
        ]

    def get_owner_url(self, obj) -> str:
        request = self.context.get("request")
        return reverse(
            "accounts-user-details", kwargs={"pk": obj.owner.pk}, request=request
        )

    def get_task_functor_url(self, obj) -> str:
        request = self.context.get("request")
        return reverse(
            "accounts-user-details", kwargs={"pk": obj.task_functor.pk}, request=request
        )

    def get_task_url(self, obj) -> str:
        request = self.context.get("request")

        return reverse("task-worker-details", kwargs={"pk": obj.pk}, request=request)


# =====================
# Admin Serializer
# =====================


class TaskAdminFullSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source="owner.username", read_only=True)
    owner_url = serializers.SerializerMethodField()
    task_functor_username = serializers.CharField(
        source="task_functor.username", read_only=True
    )
    task_functor_url = serializers.SerializerMethodField()
    task_url = serializers.SerializerMethodField()

    class Meta:
        model = Tasks
        fields = [
            "id",
            "title",
            "task",
            "owner_username",
            "owner_url",
            "task_functor",
            "task_functor_username",
            "task_functor_url",
            "created_date",
            "dead_line",
            "status",
            "worker_massage",
            "worker_task_image",
            "rejection_reason",
            "task_url",
        ]

        read_only_fields = [
            "id",
            "owner_username",
            "owner_url",
            "task_functor_username",
            "task_functor_url",
            "created_date",
            "worker_massage",
            "worker_task_image",
            "task_url",
        ]

    def get_owner_url(self, obj) -> str:
        request = self.context.get("request")
        return reverse(
            "accounts-user-details", kwargs={"pk": obj.owner.pk}, request=request
        )

    def get_task_functor_url(self, obj) -> str:
        request = self.context.get("request")
        return reverse(
            "accounts-user-details", kwargs={"pk": obj.task_functor.pk}, request=request
        )

    def get_task_url(self, obj) -> str:
        request = self.context.get("request")

        return reverse("tasks-admin-detail", kwargs={"pk": obj.pk}, request=request)


class TaskAdminSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source="owner.username", read_only=True)
    owner_url = serializers.SerializerMethodField()
    task_functor_username = serializers.CharField(
        source="task_functor.username", read_only=True
    )
    task_functor_url = serializers.SerializerMethodField()
    task_url = serializers.SerializerMethodField()

    class Meta:
        model = Tasks
        fields = [
            "id",
            "title",
            "task",
            "owner_username",
            "owner_url",
            "task_functor",
            "task_functor_username",
            "task_functor_url",
            "created_date",
            "dead_line",
            "status",
            "worker_massage",
            "worker_task_image",
            "rejection_reason",
            "task_url",
        ]

        read_only_fields = [
            "id",
            "title",
            "task",
            "owner_username",
            "owner_url",
            "task_functor",
            "task_functor_username",
            "task_functor_url",
            "created_date",
            "dead_line",
            "worker_massage",
            "worker_task_image",
            "task_url",
        ]

    def get_owner_url(self, obj) -> str:
        request = self.context.get("request")
        return reverse(
            "accounts-user-details", kwargs={"pk": obj.owner.pk}, request=request
        )

    def get_task_functor_url(self, obj) -> str:
        request = self.context.get("request")
        return reverse(
            "accounts-user-details", kwargs={"pk": obj.task_functor.pk}, request=request
        )

    def get_task_url(self, obj) -> str:
        request = self.context.get("request")

        return reverse(
            "task-admin-waiting-details", kwargs={"pk": obj.pk}, request=request
        )


class AdminChangeRoleSerializer(serializers.ModelSerializer):
    user_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "user_url", "username", "email", "role"]
        read_only_fields = ["id", "user_url", "username", "email"]

    def get_user_url(self, obj) -> str:
        request = self.context.get("request")
        return reverse(
            "change-user-roles-detail",
            kwargs={"pk": obj.pk},
            request=request,
        )


# =====================
# Full serializer
# =====================
class TasksSerializer(serializers.ModelSerializer):
    owner_url = serializers.SerializerMethodField()
    owner_username = serializers.CharField(source="owner.username", read_only=True)
    task_functor_url = serializers.SerializerMethodField()
    task_functor_username = serializers.CharField(
        source="task_functor.username", read_only=True
    )
    task_url = serializers.SerializerMethodField()

    class Meta:
        model = Tasks

        fields = [
            "task_url",
            "id",
            "title",
            "task",
            "created_date",
            "dead_line",
            "owner",
            "owner_username",
            "owner_url",
            "task_functor",
            "task_functor_username",
            "task_functor_url",
        ]
        read_only_fields = [
            "created_date",
            "owner",
            "owner_username",
            "owner_url",
            "task_functor_username",
            "task_functor_url",
        ]

    def get_task_functor_url(self, obj) -> str:
        request = self.context.get("request")
        return reverse(
            "accounts-user-details",
            kwargs={"pk": obj.task_functor.pk},
            request=request,
        )

    def get_owner_url(self, obj) -> str:
        request = self.context.get("request")
        return reverse(
            "accounts-user-details", kwargs={"pk": obj.owner.pk}, request=request
        )

    def get_task_url(self, obj) -> str:
        request = self.context.get("request")
        return reverse("task-reader-deatails", kwargs={"pk": obj.pk}, request=request)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        view = self.context.get("view")
        action = getattr(view, "action", None)
        if action == "list":
            representation.pop("url", None)
        return representation

    def get_fields(self):
        fields = super().get_fields()
        view = self.context.get("view")
        if hasattr(view, "kwargs") and view.kwargs.get("pk"):
            fields.pop("task_url", None)

        return fields
