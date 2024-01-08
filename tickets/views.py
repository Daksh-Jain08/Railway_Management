from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import random
from django.forms import formset_factory
from .models import Ticket, Passenger
from .forms import TicketBookingForm, PassengerForm
from base.models import Profile
from django.contrib.auth.decorators import login_required


tickets = []


@login_required(login_url='/login')
def TicketBookingView(request):
    message = None
    if request.method == 'POST':
        form = TicketBookingForm(request.POST)
        if form.is_valid():
            user = request.user
            trainRun = form.cleaned_data.get('train')
            date = form.cleaned_data.get('date')
            departure = form.cleaned_data.get('departure_station')
            destination = form.cleaned_data.get('destination_station')
            numberOfTickets = form.cleaned_data.get('numberOfTickets')

            train = trainRun.train
            numberOfTicketsBooked = 0

            available_seats = get_available_seats(trainRun)
            if available_seats>=numberOfTickets:
                occupied_seats = []
                booked_tickets = Ticket.objects.filter(train=trainRun)
                for booked_ticket in booked_tickets:
                    seat = booked_ticket.seatNumber
                    occupied_seats.append(seat)
                
                unoccupied_seats = []
                for i in range(train.numberOfSeats):
                    if i not in occupied_seats:
                        unoccupied_seats.append(i)

                for _ in range(numberOfTickets):
                    seat_number = random.choice(unoccupied_seats)
                    unoccupied_seats.remove(seat_number)
                    if available_seats<(numberOfTickets-numberOfTicketsBooked):
                        ticket = Ticket.objects.create(user=user, train=trainRun, date=date, departure_station=departure, destination_station=destination, seatNumber=seat_number, status='confirmed')
                    else:
                        ticket = Ticket.objects.create(user=user, train=trainRun, date=date, departure_station=departure, destination_station=destination, status='waiting')
                    tickets.append(ticket)

                return redirect('passenger-details')
            else:
                message = messages.warning(request, "You don't have sufficient ,money to book these tickets!")
            
        
        else:
            message = messages.error(request, 'Error validating Form')

    form = TicketBookingForm()
    context = {'form': form, 'message': message}
    return render(request, 'tickets/book_ticket.html', context)


def get_available_seats(train):
    tickets = Ticket.objects.filter(train=train)
    ticket_count = tickets.count()
    numberOfSeats = train.numberOfAvailableSeats
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
        train = tickets[0].train
        fare = train.fare
        profile = Profile.objects.get(user=user)
        profile.wallet -= fare*(len(tickets))
        profile.save()
        return render(request, 'tickets/booking_confirmation.html')
    
    else:
        messages.warning(request, "You are not allowed to enter that page in this manner")
        return redirect ('home')