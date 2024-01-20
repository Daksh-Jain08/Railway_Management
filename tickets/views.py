from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import random
import datetime
from .tasks import *
from django.forms import formset_factory
from .models import Ticket, Passenger
from trains.models import Train, TrainRun, Route, Schedule, SeatClass
from stations.models import Station
from .forms import TicketBookingForm, PassengerForm, RouteChoosingForm
from base.models import Profile
from django.contrib.auth.decorators import login_required
from trains.tasks import send_ticket_mail


tickets = []


@login_required(login_url='accounts/login/')
def ValidTrainsView(request):
    departure = request.GET.get('departure')
    destination = request.GET.get('destination')
    date_day = int(request.GET.get('date_day'))
    date_month = int(request.GET.get('date_month'))
    date_year = int(request.GET.get('date_year'))
    numberOfPassengers = request.GET.get('numberOfPassengers')
    seatClass = request.GET.get('seatClass')

    date = datetime.date(date_year, date_month, date_day)
    if date < datetime.date.today():
        messages.error(request, "Please choose a date that is yet to come.")
        return redirect('choose-route')
    departure_station = Station.objects.get(pk=departure)
    destination_station = Station.objects.get(pk=destination)
    trains =  Train.objects.all()
    valid_trainRuns = []
    for train in trains:
        try:
            departure_route = Route.objects.get(train=train, station=departure_station)
            destination_route = Route.objects.get(train=train, station=destination_station)
            trainRuns = TrainRun.objects.filter(train=train)
        except:
            print(train)
        else:
            print(departure_route.distance)
            print(destination_route.distance)
            if departure_route.distance < destination_route.distance:
                for trainRun in trainRuns:
                    try:
                        schedule = Schedule.objects.get(trainRun=trainRun, station=departure_station, date=date)
                        print(schedule)
                    except:
                        print('error')
                    else:
                        valid_trainRuns.append(trainRun)
    context ={'trainRuns': valid_trainRuns, 'departure': departure, 'destination': destination, 'num_tickets': numberOfPassengers, 'day': date_day, 'month': date_month, 'year': date_year, 'seatClass': seatClass}
    return render(request, 'tickets/valid_trains.html', context)

@login_required(login_url='accounts/login/')
def RouteChoosingView(request):
    tickets.clear()
    form = RouteChoosingForm()
    context = {'form': form}
    return render(request, 'tickets/route_selection.html', context)

@login_required(login_url='accounts/login/')
def TicketBookingView(request):
    user = request.user
    id = request.GET.get('pk')
    departure = request.GET.get('departure')
    destination = request.GET.get('destination')
    numberOfTickets = int(request.GET.get('num_tickets'))
    day = int(request.GET.get('day'))
    month = int(request.GET.get('month'))
    year = int(request.GET.get('year'))
    seat_class = request.GET.get('seatClass')

    date = datetime.date(year,month,day)
    departure_station = Station.objects.get(id=departure)
    destination_station = Station.objects.get(id=destination)
    trainRun = TrainRun.objects.get(id=id)
    seatClass = SeatClass.objects.get(id=seat_class)
    profile = Profile.objects.get(user=user)
    train = trainRun.train
    departure_route = Route.objects.get(train=train, station=departure_station)
    destination_route = Route.objects.get(train=train, station=destination_station)
    distance = destination_route.distance - departure_route.distance

    numberOfTicketsBooked = 0

    occupied_seats = []
    booked_tickets = Ticket.objects.filter(trainRun=trainRun, seatClass=seatClass)
    for booked_ticket in booked_tickets:
        seat = booked_ticket.seatNumber
        occupied_seats.append(seat)

    unoccupied_seats = []
    if(seatClass.seat_class=='1A'):
        fare = (train.baseFare1AC + (train.farePerKilometre*distance))*numberOfTickets
        for i in range(1, train.numberOf1AC+1):
            if i not in occupied_seats:
                unoccupied_seats.append(i)
    elif(seatClass.seat_class=='2A'):
        fare = (train.baseFare2AC + (train.farePerKilometre*distance))*numberOfTickets
        for i in range(1, train.numberOf2AC+1):
            if i not in occupied_seats:
                unoccupied_seats.append(i)
    elif(seatClass.seat_class=='3A'):
        fare = (train.baseFare3AC + (train.farePerKilometre*distance))*numberOfTickets
        for i in range(1, train.numberOf3AC+1):
            if i not in occupied_seats:
                unoccupied_seats.append(i)
    elif(seatClass.seat_class=='S'):
        fare = (train.baseFareSleeper + (train.farePerKilometre*distance))*numberOfTickets
        for i in range(1, train.numberOfSleeper+1):
            if i not in occupied_seats:
                unoccupied_seats.append(i)

    available_seats = get_available_seats(trainRun, seatClass)

    if profile.wallet>fare:
        for _ in range(numberOfTickets):
            seat_number = random.choice(unoccupied_seats)
            unoccupied_seats.remove(seat_number)
            if available_seats>=(numberOfTickets-numberOfTicketsBooked):
                ticket = Ticket.objects.create(user=user, trainRun=trainRun, date=date, departure_station=departure_station, destination_station=destination_station, seatNumber=seat_number, seatClass=seatClass, fare=fare, status='confirmed')
                numberOfTicketsBooked+=1
                if(seatClass.seat_class=='1A'):
                    trainRun.numberOfAvailable1AC-=1
                if(seatClass.seat_class=='2A'):
                    trainRun.numberOfAvailable2AC-=1
                if(seatClass.seat_class=='3A'):
                    trainRun.numberOfAvailable3AC-=1
                if(seatClass.seat_class=='S'):
                    trainRun.numberOfAvailableSleeper-=1
                trainRun.save()
            else:
                ticket = Ticket.objects.create(user=user, trainRun=trainRun, date=date, departure_station=departure_station, destination_station=destination_station, seatClass=seatClass, fare=fare, status='waiting')
            tickets.append(ticket)

        print(unoccupied_seats)
        return redirect('passenger-details')
    else:
        messages.warning(request, "You don't have sufficient money to book these tickets!")
        
    return redirect('choose-route')


def get_available_seats(trainRun, seatClass):
    tickets = Ticket.objects.filter(trainRun=trainRun, seatClass=seatClass)
    ticket_count = tickets.count()
    print(seatClass)
    if(seatClass.seat_class=='3A'):
        numberOfSeats = trainRun.numberOfAvailable1AC
    if(seatClass.seat_class=='2A'):
        numberOfSeats = trainRun.numberOfAvailable2AC
    if(seatClass.seat_class=='1A'):
        numberOfSeats = trainRun.numberOfAvailable3AC
    if(seatClass.seat_class=='S'):
        numberOfSeats = trainRun.numberOfAvailableSleeper
    
    available_seats = numberOfSeats-ticket_count
    return available_seats


def check_balance(user, train, numberOfTickets):
    print(type(user))
    profile = Profile.objects.get(user=user)
    wallet = profile.wallet
    fare = train.fare * numberOfTickets
    if fare<=wallet:
        return True
    else:
        return False


@login_required(login_url='accounts/login/')
def PassengerDetailsView(request):
    if len(tickets)!=0:
        message = None
        PassengerFormSet = formset_factory(PassengerForm, extra=len(tickets))
        if request.method == 'POST':
            formset = PassengerFormSet(request.POST)
            i=0
            for form in formset:
                if form.is_valid():
                    name = form.cleaned_data.get('name')
                    age = form.cleaned_data.get('age')
                    gender = form.cleaned_data.get('gender')
                    ticket = tickets[i]

                    passenger = Passenger.objects.create(name=name, age=age, gender=gender, ticket=ticket)
                    ticket.passenger = passenger
                    ticket.save()
                    i+=1

                else:
                    message = messages.error(request, 'Some Error Occurred!')
                    i=0
                    for _ in range(len(tickets)):
                        ticket[i].delete()
                    tickets.clear()
                    return redirect('book-ticket')
            
            return redirect('booking-confirmation')
        
        formset = PassengerFormSet()
        context = {'formset': formset, 'message': message}
        return render(request, 'tickets/passenger_details.html', context)
    
    else:
        messages.warning(request, "You are not allowed to enter that page in this manner")
        return redirect ('home')
    
    
@login_required(login_url='accounts/login/')
def BookingConfirmationView(request):
    if len(tickets)!=0:
        user = tickets[0].user
        fare = tickets[0].fare
        profile = Profile.objects.get(user=user)
        profile.wallet -= fare * len(tickets)
        profile.save()
        send_ticket_mail(user, tickets)
        tickets.clear()
        return render(request, 'tickets/booking_confirmation.html')
    
    else:
        messages.warning(request, "You are not allowed to enter that page in this manner")
        return redirect ('send-email')