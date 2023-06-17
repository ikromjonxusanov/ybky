from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from room.models import Room


class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"
