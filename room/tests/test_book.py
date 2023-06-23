import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from room.models import Book, Room


class BookCreateAPIViewTest(APITestCase):
    def setUp(self):
        Room.objects.create(name="MyTaxi", type=Room.TYPE.FOCUS, capacity=5)

    def test_create_book(self):
        url = reverse('book-create', kwargs={'pk': 1})
        data = {
            'start': '2023-07-30T09:00:00',
            'end': '2023-07-30T10:00:00',
            'resident': {
                'name': 'Ikromjon Xusanov'
            }
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.first().start, datetime.datetime(2023, 7, 30, 9, 0, 0))
        self.assertEqual(Book.objects.first().end, datetime.datetime(2023, 7, 30, 10, 0, 0))
        self.assertEqual(Book.objects.first().resident, 'Ikromjon Xusanov')

    def test_create_book_with_invalid_data(self):
        url = reverse('book-create', kwargs={'pk': 1})
        data = {
            'start': '2023-07-30T09:00:00',
            'end': '2023-07-30T08:00:00',  # Invalid end time
            'resident': {
                'name': 'Ikromjon Xusanov'
            }
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Book.objects.count(), 0)
        self.assertIn('error', response.data)
