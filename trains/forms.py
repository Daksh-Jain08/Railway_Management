from django import forms
from .models import Train, Route, Day, Schedule
from stations.models import Station

class TrainCreationForm(forms.ModelForm):

    days_of_week = forms.ModelMultipleChoiceField(
        queryset=Day.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

    numberOfStops = forms.IntegerField()

    class Meta:
        model = Train
        fields = ['trainNumber', 'trainName', 'source', 'departureTime', 'destination', 'arrivalTime', 'daysOfJourney', 'totalDistance', 'numberOf1AC', 'numberOf2AC', 'numberOf3AC', 'numberOfSleeper', 'baseFare1AC', 'baseFare2AC', 'baseFare3AC', 'baseFareSleeper', 'farePerKilometre', 'numberOfStops', 'id']

        widgets = {
            'arrivalTime': forms.TimeInput(attrs={'type': 'time'}),
            'departureTime': forms.TimeInput(attrs={'type': 'time'})
        }

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['station', 'distance']

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['daysRequiredToReach', 'arrivalTime', 'departureTime']

        widgets = {
            'arrivalTime': forms.TimeInput(attrs={'type': 'time'}),
            'departureTime': forms.TimeInput(attrs={'type': 'time'})
        }