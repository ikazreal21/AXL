import re
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *

def Home(request):
    if request.user.is_authenticated:
        if request.user.is_customer:
            return redirect('dashboard')
        else:
            return redirect('driver-dashboard')
    return render(request, 'rental/index.html')

@login_required(login_url='login')
def CustomerDashboard(request):
    return render(request, 'rental/customer/dashboard.html')
    # return render(request, 'rental/base.html')

@login_required(login_url='login')
def DriverDashboard(request):
    return render(request, 'rental/driver/driver_dashboard.html')

@login_required(login_url='login')
def CustomerBooking(request, pk):
    car = Cars.objects.get(car_id=pk)
    form = BookingForm(initial={'car': car})
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    context = {'form': form}
    return render(request, 'rental/customer/booking.html', context)




# AUTH
def Register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, f'Account was created for {user}')
            return redirect('login')
    context = {'form': form}
    return render(request, 'rental/register.html', context)

def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')
    context = {}
    return render(request, 'rental/login.html', context)

def Logout(request):
    logout(request)
    return redirect('login')