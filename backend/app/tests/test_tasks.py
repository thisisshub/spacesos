from app.models import Task
from django.test import TestCase
from app.tests.generator import TaskFactory

class TaskTestCase(TestCase):
    def setUp(self):
        self.task = TaskFactory(client=1)

    def test_task_creation(self):
        """Test if a task is created successfully."""
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(self.task.title, Task.objects.first().title)

    def test_task_completion_status(self):
        """Test that task completion defaults to False."""
        self.assertFalse(self.task.completed)

    def test_task_priority_choices(self):
        """Test that task priority is within allowed choices."""
        valid_priorities = ["low", "medium", "high"]
        self.assertIn(self.task.priority, valid_priorities)

    def test_due_date_assignment(self):
        """Test that a due date is assigned and is in the future."""
        self.assertIsNotNone(self.task.due_date)
        self.assertGreater(self.task.due_date, self.task.record_created_at)
