from django.db import models
from django.conf import settings
from app.enums import TaskPriorityEnum
from app.models.model_common_fields import BaseCommonModelDb


class Task(BaseCommonModelDb):
    TASK_PRIORITY_CHOICES = [
        (priority.value, priority.name.capitalize()) for priority in TaskPriorityEnum
    ]

    title = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tasks")
    priority = models.CharField(
        max_length=10,
        choices=TASK_PRIORITY_CHOICES,
        default=TaskPriorityEnum.MEDIUM.value,
    )

    def __str__(self):
        return f"{self.title} ({self.priority})"


class Reminder(BaseCommonModelDb):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reminders")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="reminders")
    sent = models.BooleanField(default=False)
    reminder_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Reminder for {self.task.title} on {self.reminder_time}"
