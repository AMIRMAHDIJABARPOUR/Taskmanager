from django.contrib import admin
from .models import Tasks


# Register your models here.
@admin.register(Tasks)
class TasksAdmin(admin.ModelAdmin):
    fields = [
        "title",
        "task",
        "task_functor",
        "dead_line",
        "status",
        "rejection_reason",
    ]
    list_display = ["id", "title", "owner", "task_functor", "dead_line", "status"]
    search_fields = ["title"]
    list_filter = ["created_date", "dead_line"]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.owner = request.user
        super().save_model(request, obj, form, change)
