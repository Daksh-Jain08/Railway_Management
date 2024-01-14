from django.db import models
from stations.models import Station


class Day(models.Model):
    daysChoice = [
            ('Mon', 'Monday'),
            ('Tue', 'Tuesday'),
            ('Wed', 'Wednesday'),
            ('Thu', 'Thursday'),
            ('Fri', 'Friday'),
            ('Sat', 'Saturday'),
            ('Sun', 'Sunday'),
        ]

    day_code = models.TextField(max_length=3, choices=daysChoice, default='Mon')

    def __str__(self):
        return self.day_code

class Train(models.Model):
    
    trainNumber = models.IntegerField(unique=True)
    trainName = models.CharField(max_length=100)
    source = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='source')
    departureTime = models.TimeField(null=True)
    destination = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='destination')
    arrivalTime = models.TimeField(null=True)
    daysOfJourney = models.PositiveIntegerField(null=True)
    totalDistance = models.IntegerField()
    numberOfSeats = models.PositiveIntegerField()
    daysOfWeek = models.ManyToManyField(Day, help_text='Select the days of the week', blank=True)
    baseFare = models.DecimalField(null=True, decimal_places=2, max_digits=10)
    farePerKilometre = models.DecimalField(null=True, decimal_places=2, max_digits=10)
    numberOfStops = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.trainNumber} - {self.trainName}"
    
class TrainRun(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name='train_runs')
    departure_date = models.DateField()
    arrival_date = models.DateField()
    numberOfAvailableSeats = models.IntegerField(default=12)

    def __str__(self):
        return f"Train: {self.train} - Departure: {self.departure_date} - Arrival: {self.arrival_date}"

class Schedule(models.Model):
    trainRun = models.ForeignKey(TrainRun, on_delete=models.CASCADE, related_name='schedules', null=True)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    daysRequiredToReach = models.PositiveIntegerField(default=0)
    date = models.DateField(null=True)
    arrivalTime = models.TimeField()
    departureTime = models.TimeField()

    def __str__(self):
        return f"{self.trainRun.train} - {self.station} - {self.date} - Departure: {self.departureTime}, Arrival: {self.arrivalTime}"

class Route(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name='routes')
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    distance = models.DecimalField(max_digits=8, decimal_places=2, null=True)

    class Meta:
        ordering =['distance']

    def __str__(self):
        return f"{self.train} - {self.station}"