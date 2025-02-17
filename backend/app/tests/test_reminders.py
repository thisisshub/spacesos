from django.test import TestCase
from app.models import Reminder
from app.tests.generator import ReminderFactory

class ReminderTestCase(TestCase):
    def setUp(self):
        self.reminder = ReminderFactory()

    def test_reminder_creation(self):
        """Test if a reminder is created successfully."""
        self.assertEqual(Reminder.objects.count(), 1)
        self.assertEqual(self.reminder.task.title, Reminder.objects.first().task.title)

    def test_reminder_sent_status(self):
        """Test that reminder sent status defaults to False."""
        self.assertFalse(self.reminder.sent)

    def test_reminder_time(self):
        """Test that reminder time is correctly set and in the future."""
        self.assertIsNotNone(self.reminder.reminder_time)
        self.assertGreater(self.reminder.reminder_time, self.reminder.record_created_at)
