from django.db import models


class Station(models.Model):
    stationName = models.CharField(max_length=100)
    stationCode = models.CharField(max_length=5, unique=True)

    def __str__(self):
        return f'{self.stationCode} : {self.stationName}'
