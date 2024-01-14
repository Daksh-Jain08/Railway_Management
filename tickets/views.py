from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import random
import datetime
from django.forms import formset_factory
from .models import Ticket, Passenger
from trains.models import Train, TrainRun, Route, Schedule
from stations.models import Station
from .forms import TicketBookingForm, PassengerForm, RouteChoosingForm
from base.models import Profile
from django.contrib.auth.decorators import login_required


tickets = []


@login_required(login_url='/login')
def ValidTrainsView(request):
    departure = request.GET.get('departure')
    destination = request.GET.get('destination')
    date_day = int(request.GET.get('date_day'))
    date_month = int(request.GET.get('date_month'))
    date_year = int(request.GET.get('date_year'))
    numberOfPassengers = request.GET.get('numberOfPassengers')

    date = datetime.date(date_year, date_month, date_day).isoformat()
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
            pass
        else:
            if departure_route.distance < destination_route.distance:
                for trainRun in trainRuns:
                    try:
                        schedule = Schedule.objects.get(trainRun=trainRun, station=departure_station, date=date)
                    except:
                        print("Error")
                    else:
                        valid_trainRuns.append(trainRun)
    context ={'trainRuns': valid_trainRuns, 'departure': departure, 'destination': destination, 'num_tickets': numberOfPassengers, 'date': date}
    return render(request, 'tickets/valid_trains.html', context)

@login_required(login_url='/login')
def RouteChoosingView(request):
    form = RouteChoosingForm()
    context = {'form': form}
    return render(request, 'tickets/route_selection.html', context)

@login_required(login_url='/login')
def TicketBookingView(request):
    message = None

    user = request.user
    id = request.GET.get('pk')
    date = request.GET.get('date')
    departure = request.GET.get('departure')
    destination = request.GET.get('destination')
    numberOfTickets = int(request.GET.get('num_tickets'))

    departure_station = Station.objects.get(id=departure)
    destination_station = Station.objects.get(id=destination)
    trainRun = TrainRun.objects.get(id=id)
    profile = Profile.objects.get(user=user)
    train = trainRun.train
    departure_route = Route.objects.get(train=train, station=departure_station)
    destination_route = Route.objects.get(train=train, station=destination_station)
    distance = destination_route.distance - departure_route.distance
    fare = (train.baseFare + (train.farePerKilometre*distance))*numberOfTickets
    numberOfTicketsBooked = 0

    available_seats = get_available_seats(trainRun)
    if profile.wallet>fare:
        occupied_seats = []
        booked_tickets = Ticket.objects.filter(trainRun=trainRun)
        for booked_ticket in booked_tickets:
            seat = booked_ticket.seatNumber
            occupied_seats.append(seat)
        
        unoccupied_seats = []
        for i in range(1, train.numberOfSeats):
            if i not in occupied_seats:
                unoccupied_seats.append(i)

        for _ in range(numberOfTickets):
            seat_number = random.choice(unoccupied_seats)
            unoccupied_seats.remove(seat_number)
            if available_seats>=(numberOfTickets-numberOfTicketsBooked):
                ticket = Ticket.objects.create(user=user, trainRun=trainRun, date=date, departure_station=departure_station, destination_station=destination_station, seatNumber=seat_number, status='confirmed')
            else:
                ticket = Ticket.objects.create(user=user, trainRun=trainRun, date=date, departure_station=departure_station, destination_station=destination_station, status='waiting')
            tickets.append(ticket)

        print(unoccupied_seats)
        return redirect('passenger-details')
    else:
        print(profile.wallet)
        print(type(profile.wallet))
        print(fare)
        print(type(fare))
        messages.warning(request, "You don't have sufficient ,money to book these tickets!")
        
    return redirect('choose-route')


def get_available_seats(trainRun):
    tickets = Ticket.objects.filter(trainRun=trainRun)
    ticket_count = tickets.count()
    numberOfSeats = trainRun.numberOfAvailableSeats
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


@login_required(login_url='/login')
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
                    return redirect('book-ticket')
            
            return redirect('booking-confirmation')
        
        formset = PassengerFormSet()
        context = {'formset': formset, 'message': message}
        return render(request, 'tickets/passenger_details.html', context)
    
    else:
        messages.warning(request, "You are not allowed to enter that page in this manner")
        return redirect ('home')
    
    
@login_required(login_url='/login')
def BookingConfirmationView(request):
    if len(tickets)!=0:
        user = tickets[0].user
        trainRun = tickets[0].trainRun
        train = trainRun.train
        departure_route = Route.objects.get(train=train, station=tickets[0].departure_station)
        destination_route = Route.objects.get(train=train, station=tickets[0].destination_station)
        distance = destination_route.distance - departure_route.distance
        fare = (train.baseFare + train.farePerKilometre*distance)
        profile = Profile.objects.get(user=user)
        profile.wallet -= fare*(len(tickets))
        profile.save()
        return render(request, 'tickets/booking_confirmation.html')
    
    else:
        messages.warning(request, "You are not allowed to enter that page in this manner")
        return redirect ('home')