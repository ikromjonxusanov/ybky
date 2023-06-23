from django.db import models


class Room(models.Model):
    class TYPE(models.TextChoices):
        FOCUS = 'focus'
        TEAM = 'team'
        CONFERENCE = 'conference'

    name = models.CharField(max_length=255, unique=True)
    type = models.CharField(max_length=10, choices=TYPE.choices)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Book(models.Model):
    resident = models.CharField(max_length=255)
    start = models.DateTimeField()
    end = models.DateTimeField()

    room = models.ForeignKey('room.Room', null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.resident + " " + str(self.room)
