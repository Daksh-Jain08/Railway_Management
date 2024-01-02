from django.db import models
import uuid
from stations.models import Station
from trains.models import Train, Schedule, Route
from users.models import User


class Passenger(models.Model):
    genderChoices = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    name = models.CharField(max_length=100)
    age = models.PositiveSmallIntegerField()
    gender = models.CharField(max_length=1, choices=genderChoices)

    def __str__(self):
        return f'{self.name}'


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    departure_station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='departure_tickets')
    destination_station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='destination_tickets')
    booking_time = models.DateTimeField(auto_now_add=True)
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"Ticket ID: {self.unique_id} --- {self.passenger} - {self.train} - {self.departure_station} to {self.destination_station}"