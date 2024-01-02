from django import forms
from .models import Train, Route

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

    days_of_week = forms.MultipleChoiceField(
        choices=DAYS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

    class Meta:
        model = Train
        fields = ['trainNumber', 'trainName', 'source', 'destination', 'numberOfSeats']

class RouteCreationForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = '__all__'