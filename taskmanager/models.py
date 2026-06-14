from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tasks(models.Model):
    class TaskStatus(models.TextChoices):
        DRAFT = "draft", "Draft"
        PENDING = "pending", "Pending"
        REJECTED = "rejected", "Rejected"
        FINISHED = "finished", "Finished"

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_task_manager"
    )
    title = models.CharField(max_length=512)
    task = models.TextField()
    task_functor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_task_functor"
    )
    created_date = models.DateField(auto_now_add=True)
    dead_line = models.DateField()
    worker_massage = models.TextField(default="", null=True, blank=True)
    worker_task_image = models.ImageField(null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=TaskStatus.choices, default=TaskStatus.DRAFT
    )
    rejection_reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.status})"

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
