from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from room.models import Room


class RoomListAPIViewTests(APITestCase):
    def setUp(self):
        Room.objects.create(name='MyTaxi', type='focus', capacity=5)
        Room.objects.create(name='Express24', type='team', capacity=15)
        Room.objects.create(name='Workly', type='conference', capacity=30)

    def test_get_room_list(self):
        url = reverse('rooms')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)

    def test_filter_rooms_by_type(self):
        url = reverse('rooms') + '?type=focus'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['type'], 'focus')

    def test_search_rooms_by_name(self):
        url = reverse('rooms') + '?search=MyTaxi'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'MyTaxi')


class RoomRetrieveAPIViewTests(APITestCase):
    def setUp(self):
        self.room = Room.objects.create(name='MyTaxi', type='focus', capacity=5)

    def test_get_room_details(self):
        url = reverse('room-retrieve', args=[self.room.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'MyTaxi')
        self.assertEqual(response.data['type'], 'focus')
