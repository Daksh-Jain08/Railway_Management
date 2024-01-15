from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from trains.models import Train, Route
from tickets.models import Ticket, Passenger
from tickets.forms import PassengerForm
from .models import Profile
from .forms import MoneyAddingForm

# Create your views here.

@login_required(login_url='/login')
def home(request):    
    user = request.user
    is_customer = user.is_customer
    is_staff = user.is_staff
    context = {'is_customer': is_customer, 'is_staff': is_staff}
    return render(request, 'base/home.html', context)

@login_required(login_url='/login')
def profileView(request):
    user = request.user
    tickets = Ticket.objects.filter(user=user, status='confirmed' or 'waiting')
    tickets_count = tickets.count()
    profile = Profile.objects.get(user=user)
    wallet = profile.wallet
    context = {'username': user.username, 'tickets_count': tickets_count, 'wallet': wallet}
    return render(request, 'base/profile.html', context)

@login_required(login_url='/login')
def MyTicketsView(request):
    user = request.user
    tickets = Ticket.objects.filter(user=user)
    context = {'tickets': tickets}
    return render(request, 'base/my_tickets.html', context)

@login_required(login_url='/login')
def MoneyAddingView(request):
    message = None
    if request.method == 'POST':
        form = MoneyAddingForm(request.POST)
        if form.is_valid():
            money = form.cleaned_data.get('money')
            profile = Profile.objects.get(user=request.user)
            profile.wallet += money
            profile.save()

        else:
            message = messages.error(request, "Error validating Form!")
    
    form = MoneyAddingForm()
    context = {'form': form, 'message': message}
    return render(request, 'base/money_add.html', context)


@login_required(login_url='/login')
def TicketCancellingView(request, pk):
    ticket = Ticket.objects.get(id=pk)
    if ticket.status == 'cancelled':
        messages.error(request, "The ticket is already cancelled!!")
        return redirect('my-tickets')
    user = ticket.user
    profile = Profile.objects.get(user=user)
    trainRun = ticket.trainRun
    departure_route = Route.objects.get(train=trainRun.train, station=ticket.departure_station)
    destination_route = Route.objects.get(train=trainRun.train, station=ticket.destination_station)
    distance = destination_route.distance - departure_route.distance
    fare = (trainRun.train.baseFare + (trainRun.train.farePerKilometre*distance))

    if request.user != ticket.user:
        message = messages.warning(request, "What are you trying to do? You are not allowed to do this!!")

    if request.method == 'POST':
        ticket.status = 'cancelled'
        ticket.save()
        profile.wallet += fare
        profile.save()
        message = messages.success(request, "Ticket has been canceled successfully. Money has been refunded.")
        return redirect('my-tickets')
    
    return render(request, 'delete.html', {'obj': ticket})

@login_required(login_url='/login')
def EditPassengerDetailsView(request, pk):
    message = None
    passenger = Passenger.objects.get(id=pk)
    if request.method == 'POST':
        form = PassengerForm(request.POST, instance=passenger)
        if form.is_valid():
            form.save()
            message = messages.success(request, "The pasenger details have been updated successfully.")
            return redirect('my-tickets')
        else:
            message = messages.error(request, "Error validating Form!!")
    else:
        form = PassengerForm(instance=passenger)
    context = {'form': form, 'message': message}
    return render(request, 'base/edit_passenger_details.html', context)