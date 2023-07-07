from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination


from drf_spectacular.utils import extend_schema

from .serializers import ItemSerializer, OnePieceCapituloMangaSerializer
from core.models import Item
from api.models import OnePieceCapituloManga


class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:  # Allow safe methods (GET, HEAD, OPTIONS)
            return True
        return request.user.is_staff  # Allow staff members to perform edits


class ItemViewSet(viewsets.ModelViewSet):
    """
    "Endpoint de la API que permite ver o editar, crear o eliminar los productos de la tienda"
    """
    queryset = Item.objects.all().order_by('-id')
    serializer_class = ItemSerializer
    permission_classes = [IsStaffOrReadOnly]

    @extend_schema(
        description='Obtiene una lista de todos los items disponibles en la tienda.',
        responses={200: ItemSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        """
        Obtener todos los Items
        """
        return super().list(request, *args, **kwargs)

    @extend_schema(
        description='Crea un nuevo item en la tienda.',
        request=ItemSerializer,
        responses={201: ItemSerializer()}
    )
    def create(self, request, *args, **kwargs):
        """
        Crear un Item
        """
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description='Obtiene los detalles de un item específico.',
        responses={200: ItemSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Obtener detalles de un Item
        """
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        description='Actualiza los detalles de un item específico.',
        request=ItemSerializer,
        responses={200: ItemSerializer()}
    )
    def update(self, request, *args, **kwargs):
        """
        Actualizar un Item
        """
        return super().update(request, *args, **kwargs)

    @extend_schema(
        description='Elimina un item específico de la tienda.',
        responses={204: 'No Content'}
    )
    def destroy(self, request, *args, **kwargs):
        """
        Eliminar un Item
        """
        return super().destroy(request, *args, **kwargs)


class OnePieceCapituloMangaListView(viewsets.ModelViewSet):
    queryset = OnePieceCapituloManga.objects.all()
    serializer_class = OnePieceCapituloMangaSerializer
    permission_classes = [IsStaffOrReadOnly]


pagination_class = PageNumberPagination
pagination_class.page_size = 1013