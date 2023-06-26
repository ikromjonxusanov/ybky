
from rest_framework import serializers

from room.models import Room, Book
from room.utils import BookValidation


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"


class ResidentSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)


class BookSerializer(BookValidation, serializers.ModelSerializer):
    resident = ResidentSerializer(write_only=True)
    start = serializers.DateTimeField(input_formats=['%d-%m-%Y %H:%M:%S'], write_only=True)
    end = serializers.DateTimeField(input_formats=['%d-%m-%Y %H:%M:%S'], write_only=True)

    class Meta:
        model = Book
        exclude = ('room',)

    def create(self, validated_data):
        resident = validated_data.pop('resident').get('name')
        return super().create({**validated_data, 'resident': resident})


class AvailabilitiesListSerializer(serializers.Serializer):
    start = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S')
    end = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S')
