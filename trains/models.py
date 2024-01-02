from django.db import models
from stations.models import Station


class Train(models.Model):
    trainNumber = models.IntegerField(unique=True)
    trainName = models.CharField(max_length=100)
    source = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='source')
    destination = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='destination')
    numberOfSeats = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.trainNumber} - {self.trainName}"

class Schedule(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name='schedules')
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    arrivalTime = models.DateTimeField()
    departureTime = models.DateTimeField()

    def __str__(self):
        return f"{self.train} - {self.station} - Departure: {self.departureTime}, Arrival: {self.arrivalTime}"

class Route(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name='routes')
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.train} - {self.order}. {self.station}"