from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions

from .serializers import ItemSerializer
from core.models import Item



class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:  # Allow safe methods (GET, HEAD, OPTIONS)
            return True
        return request.user.is_staff  # Allow staff members to perform edits


class ItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Item.objects.all().order_by('-id')
    serializer_class = ItemSerializer
    permission_classes = [IsStaffOrReadOnly]