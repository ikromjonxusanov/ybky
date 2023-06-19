import datetime

from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from room.serializers import RoomSerializer, BookSerializer, AvailabilitiesListSerializer
from room.models import Room, Book


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


class AvailabilityAPIView(generics.RetrieveAPIView):
    """
    Xonaning bo'sh vaqtlarini olish uchun API
    date: sana (ko'rsatilmasa bugungi sana olinadi)
    """
    queryset = Room.objects.all()

    def get(self, request, *args, **kwargs):
        date = request.query_params.get('date', datetime.date.today())
        if not isinstance(date, datetime.date):
            date = datetime.datetime.strptime(date, '%Y-%m-%d')

        date_q = Q(start__date=date) & Q(end__date=date)

        availabilities = [
            {
                'start': datetime.datetime.combine(date, datetime.time(hour=9, minute=0)),
                'end': datetime.datetime.combine(date, datetime.time(hour=18, minute=0))
            }
        ]

        books = Book.objects.filter(date_q, room=self.get_object()).values('start', 'end')
        last_book = books.last()
        if books:
            availabilities[0]['end'] = books[0]['start']

        for i in range(len(books) - 1):
            availabilities.append(
                {
                    'start': books[i]['end'],
                    'end': books[i + 1]['start']
                }
            )
            availabilities[i]['end'] = books[i]['start']

        if books and last_book['end'].hour != 18:
            availabilities.append(
                {
                    'start': last_book['end'],
                    'end': datetime.datetime.combine(date, datetime.time(hour=18, minute=0))
                }
            )

        serializers = AvailabilitiesListSerializer(availabilities, many=True)
        return Response(serializers.data)
