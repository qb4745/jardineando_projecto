from django.contrib.auth.models import User, Group
from rest_framework import serializers

from core.models import Item


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'