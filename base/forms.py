from django import forms
from .models import Profile

class MoneyAddingForm(forms.Form):
    money = forms.IntegerField()