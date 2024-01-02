from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Station
from .forms import StationCreationForm


def CreateStation(request):
    message = None
    if request.method == 'POST':
        form = StationCreationForm(request.POST)
        if form.is_valid():
            form.save()
            message = messages.success(request, 'Station created succesfully')
            return redirect('create-station')
        else:
            message = messages.error('Error validating Form')
    form = StationCreationForm()
    context = {'form': form, 'message': message}
    return render(request, 'stations/create_station.html', context)
