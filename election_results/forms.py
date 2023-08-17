from django import forms
from django.forms import fields
from .models import *

class AddPolls(forms.ModelForm):

    class Meta:
        model = New_Polling_unit
        fields = ['party','voting_category','polling_unit']

class NewPollingUnit(forms.ModelForm):

    class Meta:
        model =  New_Polling_unit
        fields = '__all__'