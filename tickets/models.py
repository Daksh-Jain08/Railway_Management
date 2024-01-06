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
    statusChoices = (
        ('waiting','Waiting'),
        ('confirmed','Confirmed'),
        ('cancelled','Cancelled')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    train = models.ForeignKey(TrainRun, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    departure_station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='departure_tickets')
    destination_station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='destination_tickets')
    booking_time = models.DateTimeField(auto_now_add=True)
    passenger = models.OneToOneField(Passenger, on_delete=models.CASCADE, null=True, related_name='tickets')
    seatNumber = models.PositiveIntegerField(null=False, default=0)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    status = models.CharField(max_length=10, choices=statusChoices, null=True)

    def __str__(self):
        return f"Ticket ID: {self.id} --- {self.passenger} - {self.train} - {self.departure_station} to {self.destination_station} - {self.status}"