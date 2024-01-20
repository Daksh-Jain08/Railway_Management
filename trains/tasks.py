from celery import shared_task
from datetime import timedelta, datetime
from django.http import FileResponse
from .models import *
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from reportlab.pdfgen import canvas

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

@shared_task
def send_ticket_mail(user, tickets):
    subject = "Booked Tickets Details"
    message = f"Your Ticket has been booked! Find the attachment"
    from_email = settings.EMAIL_HOST_USER
    if user.email != '' and user.email != None:
        recipient_list = [user.email]
    mail = EmailMessage(subject=subject,
                 body=message,
                 from_email=from_email,
                 to=recipient_list)
    
    generate_pdf_file(tickets)
    file_path = f"{settings.BASE_DIR}/ticket_details.pdf"
    mail.attach_file(file_path)
    mail.send()
    return message

def generate_pdf_file(tickets): 
    p = canvas.Canvas("ticket_details.pdf")
    p.drawString(100, 750, "Ticket Details")
    y = 700
    for ticket in tickets:
        p.drawString(100, y, f"passenegr: {ticket.passenger}")
        y -= 20
        p.drawString(100, y, f"train: {ticket.trainRun.train}")
        y -= 20
        p.drawString(100, y, f"date: {ticket.date}")
        y -= 20
        p.drawString(100, y, f"from: {ticket.departure_station}")
        y -= 20
        p.drawString(100, y, f"to: {ticket.destination_station}")
        y -= 20
        p.drawString(100, y, f"seat: {ticket.seatClass}-{ticket.seatNumber}")
        y -= 20
        p.drawString(100, y, f"status: {ticket.status}")
        y -= 20
        p.drawString(100, y, f"fare: {ticket.fare}")
        y -= 60
    p.showPage()
    p.save()