from django.shortcuts import render, redirect
from django.contrib import messages
from django.forms import formset_factory
from .models import Ticket, Passenger
from .forms import TicketBookingForm, PassengerForm

tickets = []

def TicketBookingView(request):
    message = None
    if request.method == 'POST':
        form = TicketBookingForm(request.POST)
        if form.is_valid():
            user = request.user
            train = form.cleaned_data.get('train')
            date = form.cleaned_data.get('date')
            departure = form.cleaned_data.get('departure_station')
            destination = form.cleaned_data.get('destination_station')
            numberOfTickets = form.cleaned_data.get('numberOfTickets')

            available_seats = get_available_seats(train)
            if available_seats>=numberOfTickets:
                for _ in range(numberOfTickets):
                    ticket = Ticket.objects.create(user=user, train=train, date=date, departure_station=departure, destination_station=destination)
                    tickets.append(ticket)

                return redirect('passenger-details')
            
            else:
                message = messages.error(request, f'There are only {available_seats} seats available')
        
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


def PassengerDetailsView(request):
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

def BookingConfirmationView(request):
    return render(request, 'tickets/booking_confirmation.html')