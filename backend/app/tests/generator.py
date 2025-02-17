import factory
from datetime import timedelta
from django.utils import timezone
from app.models import Task, Reminder
from django.contrib.auth.models import User


class AccountsFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating User instances with Faker.
    Reference: https://faker.readthedocs.io/en/master/#how-to-use-with-factory-boy
    """

    class Meta:
        model = User  # Django's auth user model

    username = factory.Faker("user_name")  # Generates a unique username
    email = factory.Faker("email")  # Generates a random email
    first_name = factory.Faker("first_name")  # Generates a random first name
    last_name = factory.Faker("last_name")  # Generates a random last name
    password = factory.PostGenerationMethodCall(
        "set_password", "password123"
    )  # Stores hashed password
    is_active = factory.Faker("boolean")  # Randomly active/inactive
    is_staff = False  # Default to non-staff user
    is_superuser = False  # Default to regular user

    @classmethod
    def create_superuser(cls, **kwargs):
        """
        Helper method to create a superuser.
        """
        return cls.create(is_superuser=True, is_staff=True, **kwargs)


class TaskFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating Task instances with Faker.
    """

    class Meta:
        model = Task

    title = factory.Faker("sentence", nb_words=4)  # Generates a random title
    completed = factory.Faker("boolean")  # Randomly True or False
    description = factory.Faker("paragraph")  # Generates a random paragraph
    due_date = factory.LazyFunction(
        lambda: timezone.now() + timedelta(days=7)
    )  # 7 days from now
    client = factory.SubFactory(AccountsFactory)  # Links to a user account
    priority = factory.Iterator(["low", "medium", "high"])  # Random priority


class ReminderFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating Reminder instances with Faker.
    """

    class Meta:
        model = Reminder

    client = factory.SubFactory(AccountsFactory)  # Links to a user account
    task = factory.SubFactory(TaskFactory)  # Links to a task
    sent = factory.Faker("boolean")  # Randomly True or False
    reminder_time = factory.LazyFunction(
        lambda: timezone.now() + timedelta(days=3)
    )  # 3 days from now
