from django.db import models


class Room(models.Model):
    class TYPE(models.TextChoices):
        FOCUS = 'focus'
        TEAM = 'team'
        CONFERENCE = 'conference'

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=TYPE.choices)
    capacity = models.PositiveIntegerField()
