from django.contrib import admin
from room.models import Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'capacity',)
