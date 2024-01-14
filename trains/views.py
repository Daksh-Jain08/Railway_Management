from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from .forms import TrainCreationForm, RouteForm, ScheduleForm
from .models import Train, TrainRun, Route, Schedule
from stations.models import Station
from tickets.models import Ticket
from django.contrib import messages
from datetime import timedelta

@login_required(login_url='/login')
def CreateTrain(request):
    if request.user.is_staff:
        message = None
        if request.method == 'POST':
            form = TrainCreationForm(request.POST)
            if form.is_valid():
                num_stops = form.cleaned_data.get('numberOfStops')
                train = form.save(commit=False)
                train.save()
                train.daysOfWeek.set(form.cleaned_data.get('days_of_week'))
                message = messages.success(request, 'Train successfully created')

                return redirect('create-train-route', pk=train.id, num_stops=num_stops)
            else:
                message = messages.error(request, f'{form.errors}')
        form = TrainCreationForm()
        context = {'form': form, 'messsage': message}
        return render(request, 'trains/create_train.html', context)
    
    else:
        message = messages.warning(request, "You don't have the permission to visit this page!")
        return redirect('home')


def TrainScheduleView(request, pk, num_stops):
    train = get_object_or_404(Train, id=pk)
    message = None
    routes = Route.objects.filter(train=train)
    stations = []
    for route in routes:
        station = route.station
        stations.append(station)

    ScheduleFormSet = formset_factory(ScheduleForm, extra=num_stops)
    if request.method == 'POST':
        schedule_formset = ScheduleFormSet(request.POST)
        trainRuns = TrainRun.objects.filter(train=train)
        for schedule_form in schedule_formset:
            if schedule_form.is_valid():
                i=0
                for trainRun in trainRuns:
                    schedule = schedule_form.save(commit=False)
                    schedule.station = stations[i]
                    schedule.trainRun = trainRun
                    schedule.Date = trainRun.departure_date + timedelta(days=schedule.daysRequiredToReach)
                    schedule.save()
                    i+=1
                Schedule.objects.create(trainRun=trainRun, station=train.source, daysRequiredToReach=0, Date=trainRun.departure_date, arrivalTime=train.departureTime, departureTime=train.departureTime)
                Schedule.objects.create(trainRun=trainRun, station=train.destination, daysRequiredToReach=train.daysOfJourney, Date=trainRun.arrival_date, arrivalTime=train.arrivalTime, departureTime=train.arrivalTime)
            else:
                train.delete()
                message = messages.error(request, 'Error validating form!')
        
        return redirect('all-trains')
    else:
        schedule_formset = ScheduleFormSet()
        dict = {}
        i=0
        for schedule_form in schedule_formset:
            dict[schedule_form] = stations[i]
            i+=1
    context = {'dict': dict.items(), 'message': message}
    return render(request, 'trains/create_train_schedule.html', context)

def TrainRouteView(request, pk, num_stops):
    train = get_object_or_404(Train, id=pk)
    message = None
    RouteFormSet = formset_factory(RouteForm, extra=num_stops)
    if request.method == 'POST':
        route_formset = RouteFormSet(request.POST)
        for route_form in route_formset:
            if route_form.is_valid():
                route = route_form.save(commit=False)
                route.train = train
                route.save()
            else:
                train.delete()
                message = messages.error(request, f"{route_formset.errors}")

        Route.objects.create(train=train, station=train.destination, distance=train.totalDistance)
        Route.objects.create(train=train, station=train.source, distance=0)
        return redirect('create-train-schedule', pk=train.id, num_stops=num_stops)
    else:
        route_formset = RouteFormSet()
    context = {'formset': route_formset, 'message': message}
    return render(request, 'trains/create_train_route.html', context)

@login_required(login_url='/login')
def ViewTrainRoute(request, pk):
    train = Train.objects.get(id=pk)
    train_route = Route.objects.filter(train=train).order_by('distance')

    context = {'train': train, 'train_route': train_route}
    return render(request, 'trains/view_train_route.html', context)

@login_required(login_url='/login')
def AllTicketsView(request, pk):
    user = request.user
    if user.is_staff:
        train = Train.objects.get(id=pk)
        trainRuns = TrainRun.objects.filter(train=train)
        trainRun_tickets = {}
        for trainRun in trainRuns:
            tickets = Ticket.objects.filter(trainRun=trainRun)
            trainRun_tickets[trainRun] = tickets
        
        context = {'trainRun_tickets': trainRun_tickets.items()}
        return render(request, 'trains/all_tickets.html', context)

    else:
        messages.warning(request, "You are not allowed to visit that page!!!")
        return redirect('home')
    

@login_required(login_url='/login')
def AllTrainsView(request):
    user = request.user
    if user.is_staff:
        trains = Train.objects.all()
        context = {'trains': trains}
        return render(request, 'trains/all_trains.html', context)
    
    else:
        messages.warning(request, "You are not allowed to visit that page!!!")
        return redirect('home')
    
@login_required(login_url='/login')
def EditTrianView(request, pk):
    user=request.user
    if user.is_staff:
        message = None
        train = Train.objects.get(id=pk)
        if request.method == 'POST':
            form = TrainCreationForm(request.POST, instance=train)
            if form.is_valid():
                updated_train = form.save(commit=False)
                updated_train.id=pk
                updated_train.save()
                message = messages.success(request, "The Train details have been updated successfully.")
                return redirect('all-trains')
            else:
                message = messages.error(request, "Error validating Form!!")
        else:
            form = TrainCreationForm(instance=train)
        context = {'form': form, 'message': message}
        return render(request, 'trains/create_train.html', context)
    else:
        message = messages.warning(request, "You are not allowed to visit that page!!!")
        return redirect('home')

def DeleteTrainView(request, pk):
    user = request.user
    if user.is_staff:
        message = None
        train = Train.objects.get(id=pk)
        if request.method == 'POST':
            trainRuns = TrainRun.objects.filter(train=train)
            tickets = []
            for trainRun in trainRuns:
                ticket_trainRun = Ticket.objects.filter(trainRun = trainRun)
                tickets.append(ticket_trainRun)
            
            for ticket_trainRun in tickets:
                for ticket in ticket_trainRun:
                    ticket_user = ticket.user
                    profile = ticket_user.profile
                    departure_route = Route.objects.get(train=train, station=ticket.departure_station)
                    destination_route = Route.objects.get(train=train, station=ticket.destination_station)
                    distance = destination_route.distance - departure_route.distance
                    fare = (train.baseFare + (train.farePerKilometre*distance))
                    profile.wallet += fare
                    profile.save()
            train.delete()

            messages.success(request, "Train deleted successfully.")
            return redirect('all-trains')
        
        return render(request, 'delete.html', {'obj': train})
    
    else:
        message = messages.warning(request, "You are not allowed to visit that page!!!")
        return redirect('home')
