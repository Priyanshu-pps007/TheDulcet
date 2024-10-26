from django import forms
from .models import *

class LocationForm(forms.Form):
    location = forms.CharField(max_length=255, label="Enter your location")
class OfferForm(forms.ModelForm):
    class Meta:
        model = Offers
        fields = ['title', 'description', 'image']