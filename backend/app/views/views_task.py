import structlog
from rest_framework import viewsets
from app.models import Task, Reminder
from app.serializers import TaskSerializer, ReminderSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

log = structlog.get_logger(__name__)


class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tasks to be viewed, created, updated, or deleted.
    """

    queryset = Task.objects.all().order_by("-due_date")
    serializer_class = TaskSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]  # Read-only for unauthenticated users

class ReminderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tasks to be viewed, created, updated, or deleted.
    """
    queryset = Reminder.objects.all().order_by("-reminder_time")
    serializer_class = ReminderSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]  # Read-only for unauthenticated users
