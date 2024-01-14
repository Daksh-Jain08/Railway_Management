from django.db import models
import uuid
from stations.models import Station
from trains.models import Train, Schedule, Route, TrainRun
from users.models import User

class Passenger(models.Model):
    genderChoices = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    name = models.CharField(max_length=100)
    age = models.PositiveSmallIntegerField()
    gender = models.CharField(max_length=1, choices=genderChoices)
    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE, null=True, blank=True, related_name='passengers')

    def __str__(self):
        return f'{self.name}'


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    trainRun = models.ForeignKey(TrainRun, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    departure_station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='departure_tickets')
    destination_station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='destination_tickets')
    booking_time = models.DateTimeField(auto_now_add=True)
    passenger = models.OneToOneField(Passenger, on_delete=models.CASCADE, null=True, related_name='tickets')
    seatNumber = models.PositiveIntegerField(null=False, default=0)
    status = models.CharField(max_length=10, null=True)

    def __str__(self):
        return f"Ticket ID: {self.id} --- {self.user} --- {self.passenger} - {self.trainRun.train}, Departure: {self.departure_station}, Destination {self.destination_station}, Seat Number: {self.seatNumber}, status: {self.status}"