from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter

from room.serializers import RoomSerializer
from room.models import Room


class RoomListAPIView(generics.ListAPIView):
    serializer_class = RoomSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['type']
    search_fields = ['name']
    queryset = Room.objects.all().order_by('id')


class RoomRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()
