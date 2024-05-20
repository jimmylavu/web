from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class PlanForm(forms.ModelForm):

    class Meta:
        model = Plan
        fields = '__all__'

class CreateUSerForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = '__all__'