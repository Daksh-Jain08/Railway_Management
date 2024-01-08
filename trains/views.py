from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import TrainCreationForm
from .models import Train, TrainRun
from tickets.models import Ticket
from django.contrib import messages

@login_required(login_url='/login')
def CreateTrain(request):
    if request.user.is_staff:
        message = None
        if request.method == 'POST':
            form = TrainCreationForm(request.POST)
            if form.is_valid():
                form.save()
                message = messages.success(request, 'Train successfully created')
                return redirect('create-train')
            else:
                message = messages.error(request, 'Error in validating form.')
        form = TrainCreationForm()
        context = {'form': form, 'messsage': message}
        return render(request, 'trains/create_train.html', context)
    
    else:
        message = messages.warning(request, "You don't have the permission to visit this page!")
        return redirect('home')
    

@login_required(login_url='/login')
def AllTicketsView(request, pk):
    user = request.user
    if user.is_staff:
        train = Train.objects.get(id=pk)
        trainRuns = TrainRun.objects.filter(train=train)
        trainRun_tickets = {}
        for trainRun in trainRuns:
            tickets = Ticket.objects.filter(train=trainRun)
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
        train = get_object_or_404(Train, id=pk)
        if request.method == 'POST':
            trainRuns = TrainRun.objects.filter(train=train)
            tickets = []
            for trainRun in trainRuns:
                ticket_trainRun = Ticket.objects.filter(train = trainRun)
                tickets.append(ticket_trainRun)
            
            for ticket_trainRun in tickets:
                for ticket in ticket_trainRun:
                    ticket_user = ticket.user
                    profile = ticket_user.profile
                    profile.wallet += train.fare
                    profile.save()
            train.delete()

            messages.success(request, "Train deleted successfully.")
            return redirect('all-trains')
        
        return render(request, 'delete.html', {'obj': train})
    
    else:
        message = messages.warning(request, "You are not allowed to visit that page!!!")
        return redirect('home')
