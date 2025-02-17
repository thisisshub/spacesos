from uuid import uuid4
from django.db import models


class BaseCommonModelDb(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    record_created_at = models.DateTimeField(auto_now_add=True)  # Set when created
    record_updated_at = models.DateTimeField(auto_now=True)  # Auto updates on modification
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True