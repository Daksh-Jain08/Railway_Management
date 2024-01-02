from django.db import models
from stations.models import Station


class Train(models.Model):
    daysChoice = [
            ('Mon', 'Monday'),
            ('Tue', 'Tuesday'),
            ('Wed', 'Wednesday'),
            ('Thu', 'Thursday'),
            ('Fri', 'Friday'),
            ('Sat', 'Saturday'),
            ('Sun', 'Sunday'),
        ]

    trainNumber = models.IntegerField(unique=True)
    trainName = models.CharField(max_length=100)
    source = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='source')
    destination = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='destination')
    numberOfSeats = models.PositiveIntegerField()
    daysOfWeek = models.CharField(max_length=20, choices=daysChoice, help_text='Select the days of the week', blank=True)

    def get_days_list(self):
        return [day[0] for day in self.daysChoice if day[0] in self.daysOfWeek]

    def set_days_list(self, daysList):
        self.daysOfWeek = ','.join(daysList)

    daysList = property(get_days_list, set_days_list)

    def __str__(self):
        return f"{self.trainNumber} - {self.trainName}"
    
class TrainRun(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name='train_runs')
    departure_date = models.DateField()
    arrival_date = models.DateField()

    def __str__(self):
        return f"TrainRun for Train: {self.train} - Departure: {self.departure_date} - Arrival: {self.arrival_date}"

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
    distance = models.DecimalField(max_digits=8, decimal_places=2, null=True)

    def __str__(self):
        return f"{self.train} - {self.order}. {self.station}"