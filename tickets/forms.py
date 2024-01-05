from django import forms
from django.forms import formset_factory
from django.db import transaction
from .models import Ticket, Passenger
from trains.models import TrainRun

class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = ['name', 'age', 'gender']

class TicketBookingForm(forms.ModelForm):
    numberOfTickets = forms.IntegerField()

    class Meta:
        model = Ticket
        fields = ['train', 'date', 'departure_station', 'destination_station']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }