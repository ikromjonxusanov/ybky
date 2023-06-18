import datetime

from rest_framework import serializers
from room.models import Room, Book


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"


class ResidentSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)


class BookSerializer(serializers.ModelSerializer):
    resident = ResidentSerializer(write_only=True)

    class Meta:
        model = Book
        exclude = ('room',)
        extra_kwargs = {
            'start': {'write_only': True},
            'end': {'write_only': True}
        }

    def validate(self, attrs):
        now = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)
        room_id = self.context.get('view').kwargs.get('pk')
        start = attrs.get('start')
        end = attrs.get('end')

        availabilities = [
            {'start': now.replace(hour=9), 'end': now.replace(hour=11)},
            {'start': now.replace(hour=13), 'end': now.replace(hour=18)}
        ]

        if now > start or now > end or end < start:
            raise serializers.ValidationError({"error": "Iltimos to'g'ri vatq kiriting"})

        for availability in availabilities:
            if availability['start'] <= start <= availability['end'] and \
                    availability['start'] <= end <= availability['end']:
                break
        else:
            raise serializers.ValidationError({"error": "Iltimos to'g'ri vatq kiriting"})

        if Book.objects.filter(
                room_id=room_id,
                start__range=[start, end]
        ).exists():
            raise serializers.ValidationError(
                {"error": "uzr, siz tanlagan vaqtda xona band"},
            )

        return attrs

    def create(self, validated_data):
        resident = validated_data.pop('resident').get('name')
        return super().create({**validated_data, 'resident': resident})
