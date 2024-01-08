from django import forms
from .models import Train, Route, Day
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
        fields = ['trainNumber', 'trainName', 'source', 'destination','totalDistance', 'numberOfSeats', 'fare', 'id']

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['station', 'distance']