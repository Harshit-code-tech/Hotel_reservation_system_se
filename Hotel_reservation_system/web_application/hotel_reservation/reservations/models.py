from djongo import models

class Room(models.Model):
    room_number = models.CharField(max_length=10)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)

class Hotel(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    rooms = models.ArrayField(model_container=Room)
