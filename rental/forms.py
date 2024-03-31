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

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user', 'customer_id']
    
class DriverForm(ModelForm):
    class Meta:
        model = Driver
        fields = '__all__'
        exclude = ['user', 'driver_id']

class CarForm(ModelForm):
    class Meta:
        model = Cars
        fields = '__all__'
        exclude = ['car_id']