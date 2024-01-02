from django import forms
from .models import Station

class StationCreationForm(forms.ModelForm):
    class Meta:
        model = Station
        fields = '__all__'