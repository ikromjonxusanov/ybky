from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter

from room.mixins import AvailabilityMixin
from room.serializers import RoomSerializer, BookSerializer
from room.models import Room


class RoomListAPIView(generics.ListAPIView):
    """
    Mavjud xonalarni olish uchun API

    search: Xona nomi orqali qidirish
    type: xona turi bo'yicha saralash (focus, team, conference)
    page: sahifa tartib raqami
    page_size: sahifadagi maksimum natijalar soni
    """
    serializer_class = RoomSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['type']
    search_fields = ['name']
    queryset = Room.objects.all().order_by('id')


class RoomRetrieveAPIView(generics.RetrieveAPIView):
    """
    Xonani id orqali olish uchun API
    """
    serializer_class = RoomSerializer
    queryset = Room.objects.all()


class BookCreateAPIView(generics.CreateAPIView):
    """
    Xonani band qilish uchun API
    """
    serializer_class = BookSerializer

    def perform_create(self, serializer):
        serializer.save(room_id=self.kwargs.get('pk'))


class AvailabilityAPIView(AvailabilityMixin, generics.RetrieveAPIView):
    """
    Xonaning bo'sh vaqtlarini olish uchun API
    date: sana (ko'rsatilmasa bugungi sana olinadi)
    """
    queryset = Room.objects.all()
