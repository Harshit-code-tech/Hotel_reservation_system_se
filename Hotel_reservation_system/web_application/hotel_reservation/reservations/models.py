from djongo import models

class Room(models.Model):
    room_number = models.IntegerField()
    room_type = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        abstract = True  # Mark as abstract to embed within Hotel

    def __str__(self):
        return f"Room {self.room_number} - {self.room_type}"

class Hotel(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    rooms = models.ArrayField(
        model_container=Room,
    )

    def __str__(self):
        return self.name

