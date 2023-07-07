from django.contrib.auth.models import User, Group
from rest_framework import serializers

from core.models import Item
from .models import OnePieceCapituloManga


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class OnePieceCapituloMangaSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnePieceCapituloManga
        fields = '__all__'
        lookup_field = 'capitulo'


