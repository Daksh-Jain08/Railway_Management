from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Station
from .forms import StationCreationForm

@login_required(login_url='accounts/login/')
def CreateStation(request):
    if request.user.is_staff:
        message = None
        if request.method == 'POST':
            form = StationCreationForm(request.POST)
            if form.is_valid():
                form.save()
                message = messages.success(request, 'Station created succesfully')
                return redirect('create-station')
            else:
                message = messages.error(request, form.errors)
        form = StationCreationForm()
        context = {'form': form, 'message': message}
        return render(request, 'stations/create_station.html', context)
    
    else:
        message = messages.warning(request, "You don't have the permission to visit that page!")
        return redirect('home')
