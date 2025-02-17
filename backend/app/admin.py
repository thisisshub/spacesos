from django.contrib import admin
from django.apps import apps

# Get all models from the current app
# -----------------------------------
app_models = apps.get_models()

for model in app_models:
    class GenericAdmin(admin.ModelAdmin):
        list_display = [
            field.name for field in model._meta.fields
        ]  # Display all fields
        search_fields = [
            field.name
            for field in model._meta.fields
            if field.get_internal_type() in ["CharField", "TextField"]
        ]  # Searchable text fields
        list_filter = [
            field.name
            for field in model._meta.fields
            if field.get_internal_type()
            in ["BooleanField", "DateField", "DateTimeField"]
        ]  # Filters for relevant fields

    # Register model with its admin class
    # -----------------------------------
    try:
        admin.site.register(model, GenericAdmin)
    except admin.sites.AlreadyRegistered:
        pass
