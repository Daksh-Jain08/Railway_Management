from django import forms
from .models import Train, Route

class TrainCreationForm(forms.ModelForm):
    class Meta:
        model = Train
        fields = '__all__'

class RouteCreationForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = '__all__'