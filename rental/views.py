import re
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from datetime import datetime


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
    car = Cars.objects.all()
    context = {'cars': car}
    return render(request, 'rental/customer/dashboard.html', context)
    # return render(request, 'rental/base.html')

@login_required(login_url='login')
def DriverDashboard(request):
    return render(request, 'rental/driver/driver_dashboard.html')

@login_required(login_url='login')
def CustomerBooking(request, car_id):
    driver = Driver.objects.all()
    car = Cars.objects.get(car_id=car_id)
    customer = Customer.objects.get(user=request.user)

    form = BookingForm()
    if request.method == 'POST':
        is_toll = request.POST.get("is_toll")
        is_cash = request.POST.get("gridRadios")
        start = request.POST.get("booking_start_date")
        end = request.POST.get("booking_end_date")
        a = datetime.strptime(start, '%Y-%m-%d')
        b = datetime.strptime(end, '%Y-%m-%d')
        delta = b - a
        print(is_toll, start, end, delta.days)
        form = BookingForm(request.POST, request.FILES)
        print(form)
        if form.is_valid() and delta.days > 0:
            form.save(commit=False).customer = customer
            form.save(commit=False).car = car
            form.save(commit=False).booking_start_date = start
            form.save(commit=False).booking_end_date = end
            form.save(commit=False).booking_status = "Pending"
            if is_cash == "true":
                form.save(commit=False).is_cash = True
            calculate_total = form.save()
            if is_toll == "true":
                calculate_total.booking_total_price += calculate_total.toll_fee
            total = delta.days * car.car_price
            print(total)
            calculate_total.booking_total_price += total
            calculate_total.save()
            return redirect('dashboard')
        else:
            system_messages = messages.get_messages(request)
            for message in system_messages:
                # This iteration is necessary
                pass
            messages.error(request, "Invalid Date")
            context = {'form': form, "car": car , "drivers": driver}
            return render(request, 'rental/customer/booking.html', context)
    context = {'form': form, "car": car , "drivers": driver}
    return render(request, 'rental/customer/booking.html', context)


@login_required(login_url='login')
def PendingBooking(request):
    booking = Booking.objects.filter(booking_status="Pending")
    context = {'bookings': booking}
    return render(request, 'rental/customer/pending_booking.html', context)

@login_required(login_url='login')
def BookingHistory(request):
    booking = Booking.objects.filter(booking_status="Confirmed")
    context = {'bookings': booking}
    return render(request, 'rental/customer/booking_history.html', context)

@login_required(login_url='login')
def CurrentBooking(request):
    booking = Booking.objects.filter(booking_status="Confirmed")
    context = {'bookings': booking}
    return render(request, 'rental/customer/current_booking.html', context)

@login_required(login_url='login')
def ReturnCar(request, booking_id):
    booking = Booking.objects.get(booking_id=booking_id)
    booking.booking_status = "Returned"
    booking.save()
    return redirect('dashboard')

@login_required(login_url='login')
def BookingDetails(request, booking_id):
    booking = Booking.objects.get(booking_id=booking_id)
    context = {'booking': booking}
    return render(request, 'rental/customer/booking_details.html', context)

@login_required(login_url='login')
def ConfirmBooking(request, booking_id):
    booking = Booking.objects.get(booking_id=booking_id)
    booking.booking_status = "Confirmed"
    booking.save()
    return redirect('pending-booking')


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


# Terms and Conditions
def TermsAndConditions(request):
    return render(request, 'rental/termsandcondition.html')