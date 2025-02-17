from rest_framework import viewsets
from app.serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated


class UsersViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed, created, updated, or deleted.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Restrict users to see only their own profile."""
        return User.objects.filter(id=self.request.user.id)

    def get_permissions(self):
        """Set different permissions for different actions."""
        if self.action == "create":
            return [AllowAny()]  # Anyone can create an account
        return [IsAuthenticated()]  # Auth required for other actions
    