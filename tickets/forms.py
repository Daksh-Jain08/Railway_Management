from django import forms
from stations.models import Station
from .models import Ticket, Passenger

class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = ['name', 'age', 'gender']

class TicketBookingForm(forms.ModelForm):
    numberOfTickets = forms.IntegerField()

    class Meta:
        model = Ticket
        fields = ['trainRun', 'date', 'departure_station', 'destination_station']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class RouteChoosingForm(forms.Form):
    departure = forms.ModelChoiceField(queryset=Station.objects.all())
    destination = forms.ModelChoiceField(queryset=Station.objects.all())
    date = forms.DateField(widget=forms.SelectDateWidget)
    numberOfPassengers = forms.IntegerField()
    widgets = {
        'date': forms.SelectDateWidget(),
    }