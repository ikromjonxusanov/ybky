from django.utils import timezone

from django.test import TestCase
from room.models import Room, Book


class RoomModelTest(TestCase):

    def setUp(self):
        self.room = Room.objects.create(
            name='Express24',
            type=Room.TYPE.FOCUS,
            capacity=10
        )

    def test_room_str_representation(self):
        expected_str = 'Express24'
        self.assertEqual(str(self.room), expected_str)

    def test_room_type_choices(self):
        self.assertEqual(Room.TYPE.FOCUS, 'focus')
        self.assertEqual(Room.TYPE.TEAM, 'team')
        self.assertEqual(Room.TYPE.CONFERENCE, 'conference')

    def test_room_capacity_positive(self):
        self.assertGreater(self.room.capacity, 0)

    def test_room_name_unique(self):
        duplicate_room = Room(
            name='Express24',
            type=Room.TYPE.FOCUS,
            capacity=10
        )
        with self.assertRaises(Exception):
            duplicate_room.save()


class BookModelTests(TestCase):
    def setUp(self):
        self.room = Room.objects.create(name='MyTaxi', capacity=10, type=Room.TYPE.FOCUS)
        self.book = Book.objects.create(
            resident='Ikromjon Xusanov',
            start=timezone.now(),
            end=timezone.now(),
            room=self.room
        )

    def test_book_create(self):
        self.assertEqual(str(self.book), self.book.resident + " " + str(self.book.room))

    def test_book_room_null(self):
        book_without_room = Book.objects.create(
            resident='Ikromjon Xusanov',
            start=timezone.now(),
            end=timezone.now()
        )
        self.assertIsNone(book_without_room.room)

    def test_book_foreign_key(self):
        self.assertEqual(self.book.room, self.room)

    def test_book_start_end(self):
        self.assertIsInstance(self.book.start, timezone.datetime)
        self.assertIsInstance(self.book.end, timezone.datetime)
