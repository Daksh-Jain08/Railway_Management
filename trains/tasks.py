from celery import shared_task
from datetime import timedelta, datetime
from .models import *

@shared_task
def schedule():
    trains = Train.objects.all()
    
    today = datetime.today()
    for train in trains:
        train_days = set(train.daysOfWeek.values_list('day_code', flat=True))
        if today.strftime('%a') in train_days:
                TrainRun.objects.create(
                    train=train,
                    departure_date=today,
                    arrival_date=today + timedelta(days=train.daysOfJourney),
                    numberOfAvailable1AC=train.numberOf1AC,
                    numberOfAvailable2AC=train.numberOf2AC,
                    numberOfAvailable3AC=train.numberOf3AC,
                    numberOfAvailableSleeper=train.numberOfSleeper,
                )

    for train in trains:
         routes = Route.objects.filter(train=train)
         trainRuns = TrainRun.objects.fliter(train=train, date=today)
         for trainRun in trainRuns:
              for route in routes:
                   schedule = Schedule.objects.get(trainRun=trainRun,station=route.station)
                   daysRequiredToReach = schedule.daysRequiredToReach
                   date = today + timedelta(days=daysRequiredToReach)
                   Schedule.objects.create(trainRun=trainRun, station=route.station, date=date, daysRequiredToReach=daysRequiredToReach, arrivalTime=schedule.arrivalTime, departureTime=schedule.departureTime)

    return "Done"