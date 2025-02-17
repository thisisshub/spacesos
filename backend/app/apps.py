import os
import structlog
from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.db.utils import OperationalError, ProgrammingError

log = structlog.get_logger(__name__)


class AppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"

    def ready(self):
        if os.environ.get("RUN_MAIN") == "true":  # Ensures it runs only once
            try:
                User = get_user_model()
                email = os.getenv("DJANGO_SUPERUSER_EMAIL")
                username = os.getenv("DJANGO_SUPERUSER_USERNAME")
                password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

                if not User.objects.filter(username=username).exists():
                    User.objects.create_superuser(
                        username=username, email=email, password=password
                    )
                    print(f"Superuser '{username}' created successfully!")
            except (OperationalError, ProgrammingError):
                pass  # Handles migrations not being applied yet
