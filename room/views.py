from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter

from room.serializers import RoomListSerializer
from room.models import Room


class RoomListAPIView(generics.ListAPIView):
    serializer_class = RoomListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['type']
    search_fields = ['name']
    queryset = Room.objects.all().order_by('id')
