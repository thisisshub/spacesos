from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenVerifyView,
    TokenRefreshView,
    TokenObtainPairView,
)
from app.views.views_users import UsersViewSet
from app.views.views_task import (
    TaskViewSet,
    ReminderViewSet,
)
from app.views.view_reports import (
    ReportView,
    PriorityTaskView,
    ClientReminderView,
    AdvisorQuerySuggestionView,
)

# -----------------------------------------------------
# Create API router
# -----------------------------------------------------
router = DefaultRouter()
router.register(r"tasks", TaskViewSet, basename="task")
router.register(r"users", UsersViewSet, basename="users")
router.register(r"reminders", ReminderViewSet, basename="reminder")

urlpatterns = [
    # -----------------------------------------------------
    # Admin Endpoint
    # -----------------------------------------------------
    path("admin/", admin.site.urls),
    # -----------------------------------------------------
    # Authentication Endpoints
    # -----------------------------------------------------
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # -----------------------------------------------------
    # Router Enpoints
    # -----------------------------------------------------
    path("api/", include(router.urls)),  # Include DRF router
    # -----------------------------------------------------
    # Reports API Routes Enpoints
    # -----------------------------------------------------
    path(
        "api/reports/daily-reports/", 
         ReportView.as_view(), 
         name="daily-reports"),
    path(
        "api/reports/priority-tasks/", 
        PriorityTaskView.as_view(), 
        name="priority-tasks"
    ),
    path(
        "api/reports/client-reminders/",
        ClientReminderView.as_view(),
        name="client-reminders",
    ),
    path(
        "api/reports/advisor-queries/",
        AdvisorQuerySuggestionView.as_view(),
        name="advisor-queries",
    ),
]
