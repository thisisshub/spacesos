import re
import dateparser
from backend.settings import log
from app.models import Task, Reminder
from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils.timezone import make_aware
from datetime import datetime, timedelta, timezone


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """Ensure the user is created as active."""
        user = User.objects.create_user(**validated_data)
        user.is_active = True  # Ensure the user is active
        user.save()
        return user


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for Tasks, automatically creating a reminder when a new task is added.
    """

    reminder_created = serializers.BooleanField(default=False, read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "completed",
            "due_date",
            "priority",
            "client",
            "reminder_created",
        ]

    def extract_reminder_date(self, text):
        """
        Extracts explicit and relative dates from the task title.
        """
        # Regex to detect explicit dates (e.g., "on 18th Feb", "on March 10")
        date_pattern = r"(?:on\s+)?(\d{1,2}(?:st|nd|rd|th)?\s+\w+|\w+\s+\d{1,2})"

        # List of relative date keywords
        relative_dates = [
            "tomorrow", "next monday", "next tuesday", "next wednesday", "next thursday",
            "next friday", "next saturday", "next sunday"
        ]

        # Step 1: Search for explicit dates in task title (e.g., "on 18th Feb")
        match = re.search(date_pattern, text, re.IGNORECASE)
        if match:
            extracted_date = dateparser.parse(match.group(1), settings={"PREFER_DATES_FROM": "future"})
            if extracted_date:
                return make_aware(extracted_date)

        # Step 2: Check for relative dates (e.g., "next monday", "tomorrow")
        for rel_date in relative_dates:
            if rel_date in text.lower():
                extracted_date = dateparser.parse(rel_date, settings={"PREFER_DATES_FROM": "future"})
                if extracted_date:
                    return make_aware(extracted_date)

        return None

    def create(self, validated_data):
        """
        Creates a task and automatically generates a reminder based on the task title.
        """
        request = self.context.get("request")  # Get request context
        user = request.user if request else None

        if not user or not user.is_authenticated:
            raise serializers.ValidationError("User authentication required to create a task.")

        task = Task.objects.create(**validated_data)

        # Extract reminder date from task title
        reminder_time = self.extract_reminder_date(task.title)

        # Default to tomorrow if no valid date is found
        if not reminder_time:
            reminder_time = make_aware(datetime.now() + timedelta(days=1))

        # Create Reminder only if it doesn't exist
        if not Reminder.objects.filter(task=task).exists():
            Reminder.objects.create(client=user, task=task, reminder_time=reminder_time)

        return task

    def update(self, instance, validated_data):
        """
        Override the default `update` method to automatically update the related reminder
        whenever a task is updated.
        """
        # Extract the title if it has changed (or any other fields you might want to watch)
        new_title = validated_data.get('title', instance.title)

        # Now, we check if the title was changed and update the related reminder.
        if new_title != instance.title:
            # Extract the reminder date from the updated title
            reminder_time = self.extract_reminder_date(new_title)

            # Default to tomorrow if no valid date is found
            if not reminder_time:
                reminder_time = make_aware(datetime.now() + timedelta(days=1))

            # Update the related Reminder object
            reminder = Reminder.objects.filter(task=instance).first()
            if reminder:
                reminder.reminder_time = reminder_time
                reminder.save()

        # Update the Task instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return instance

class ReminderSerializer(serializers.ModelSerializer):
    """
    Serializer for Reminders, automatically setting task and client.
    """

    class Meta:
        model = Reminder
        fields = "__all__"
