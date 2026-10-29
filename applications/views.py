from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Application
from .serializers import ApplicationSerializer


class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only MY applications
        return Application.objects.filter(owner=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        # New applications belong to ME
        serializer.save(owner=self.request.user)