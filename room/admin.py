from django.contrib import admin
from room.models import Room, Book


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'capacity',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'room', 'resident', 'start', 'end')
