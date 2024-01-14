from django import forms
from .models import Train, Route, Day, Schedule
from stations.models import Station

class TrainCreationForm(forms.ModelForm):
    DAYS_CHOICES = [
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
        ('Sat', 'Saturday'),
        ('Sun', 'Sunday'),
    ]

    days_of_week = forms.ModelMultipleChoiceField(
        queryset=Day.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

    numberOfStops = forms.IntegerField()

    class Meta:
        model = Train
        fields = ['trainNumber', 'trainName', 'source', 'destination', 'daysOfJourney', 'totalDistance', 'numberOfSeats', 'baseFare', 'farePerKilometre', 'numberOfStops', 'id']

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['station', 'distance']

query = Station.objects.none()

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['daysRequiredToReach', 'arrivalTime', 'departureTime']

        widgets = {
            'arrivalTime': forms.TimeInput(attrs={'type': 'time'}),
            'departureTime': forms.TimeInput(attrs={'type': 'time'})
        }