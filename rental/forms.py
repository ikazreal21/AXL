from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.forms import ModelForm, ValidationError
from .models import *


class CreateUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
    

class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'
        exclude = ['booking_id', 'customer']
        widgets = {
            'car': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        car = cleaned_data.get('car')
        start_dates = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_dates and end_date and start_dates > end_date:
            raise ValidationError("End date must be greater than start date")
        return cleaned_data