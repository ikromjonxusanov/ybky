from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter

from room.serializers import RoomSerializer, BookSerializer
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


class BookCreateAPIView(generics.CreateAPIView):
    serializer_class = BookSerializer

    def perform_create(self, serializer):
        serializer.save(room_id=self.kwargs.get('pk'))
