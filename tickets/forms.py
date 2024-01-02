from django import forms
from django.forms import formset_factory
from django.db import transaction
from .models import Ticket, Passenger
from trains.models import TrainRun

class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = ['name', 'age', 'gender']

