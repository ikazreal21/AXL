from dataclasses import is_dataclass
from lib2to3.pgen2 import driver
from multiprocessing import context
from operator import inv
import re
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from datetime import date, datetime
from pytz import timezone

import requests 
from django.db.models import Q

from .models import *
from .forms import *

def Home(request):
    car = Cars.objects.filter(is_available=True).all()
    # date = datetime.now()
    # print(date.date())
    context = {'cars': car}
    if request.user.is_authenticated:
        if request.user.is_customer:
            return redirect('dashboard')
        else:
            return redirect('driver-dashboard')
        
    return render(request, 'rental/index.html' , context)

@login_required(login_url='login')
def CustomerDashboard(request):
    car = Cars.objects.filter(is_available=True).all()
    # date = datetime.now()
    # print(date.date())
    context = {'cars': car}
    return render(request, 'rental/customer/dashboard.html', context)
    # return render(request, 'rental/base.html')

@login_required(login_url='login')
def DriverDashboard(request):
    driver = Driver.objects.get(user=request.user)
    booking = Booking.objects.filter(driver=driver).filter(booking_status="Confirmed")
    context = {'bookings': booking}
    return render(request, 'rental/driver/driver_dashboard.html', context)

@login_required(login_url='login')
def CustomerBooking(request, car_id):
    driver = Driver.objects.all()
    car = Cars.objects.get(car_id=car_id)
    customer = Customer.objects.get(user=request.user)

    form = BookingForm()
    if request.method == 'POST':
        is_toll = request.POST.get("is_toll")
        is_cash = request.POST.get("gridRadios")
        is_driver = request.POST.get("is_driver")
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
            car.is_available = False
            car.save()
            if is_driver == "on":
                print("Driver")
                driver = request.POST.get("driver")
                driver = Driver.objects.get(driver_id=driver)
                carprice = car.car_price + driver.driver_price
                form.save(commit=False).driver = driver
                print(driver.driver_price)
                print(carprice)
            else:
                carprice = car.car_price
            calculate_total = form.save()
            if is_toll == "on":
                calculate_total.booking_total_price += calculate_total.toll_fee
            total = delta.days * carprice
            print(carprice)
            print(total)
            calculate_total.booking_total_price += total
            if is_cash == "true":
                calculate_total.is_cash = True
                calculate_total.save()
            else:
                calculate_total.save()
                return redirect('billing', booking_id=calculate_total.booking_id)
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
    booking = Booking.objects.filter(booking_status="Returned")
    context = {'bookings': booking}
    return render(request, 'rental/customer/booking_history.html', context)

@login_required(login_url='login')
def CurrentBooking(request):
    booking = Booking.objects.filter(booking_status="Confirmed")
    context = {'bookings': booking}
    return render(request, 'rental/customer/return_mycar.html', context)

@login_required(login_url='login')
def LateReturnBooking(request):
    booking = Booking.objects.filter(booking_status="Late")
    context = {'bookings': booking}
    return render(request, 'rental/customer/penalty_to_pay.html', context)

@login_required(login_url='login')
def ReturnCar(request, booking_id):
    booking = Booking.objects.get(booking_id=booking_id)
    end = booking.booking_end_date
    date = datetime.now(timezone('Asia/Manila'))
    end_date = datetime.strptime(str(end), '%Y-%m-%d')
    current_date = datetime.strptime(str(date.date()), '%Y-%m-%d')
    delta = current_date - end_date
    if delta.days > 0:
        booking.total_penalty = delta.days * 5000
        booking.booking_status = "Late"
    else:
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

@login_required(login_url='login')
def Billing(request, booking_id):
    booking = Booking.objects.get(booking_id=booking_id)
    if request.method == 'POST':
        reference_number = request.POST.get("reference_number")
        if booking.booking_status == "Late": 
           booking.reference_number_penalty = reference_number
           booking.booking_status = "Returned"
        else:    
            booking.reference_number = reference_number
        booking.save()
        return redirect('dashboard')
    context = {'booking': booking}
    return render(request, 'rental/customer/billing.html', context)

def CancelBooking(request, booking_id):
    booking = Booking.objects.get(booking_id=booking_id)
    car = Cars.objects.get(car_id=booking.car.car_id)
    car.is_available = True
    car.save()
    booking.delete()
    return redirect('dashboard')

def Invoice(request, booking_id):
    booking = Booking.objects.get(booking_id=booking_id)
    date = datetime.now(timezone('Asia/Manila'))
    invoice_number = str(booking.booking_id)
    invoice_number = invoice_number.split("-")
    print(invoice_number)
    context = {'booking': booking, 'date': date.strftime("%B %d, %Y") , 'invoice_number': invoice_number[0]}
    return render(request, 'rental/customer/invoice.html', context)

@login_required(login_url='login')
def CustomerProfile(request):
    customer = Customer.objects.get(user=request.user)
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save(commit=False).is_first_time = False
            form.save()
            return redirect('dashboard')
    context = {'form': form, 'customer': customer}
    return render(request, 'rental/customer/profile_customer.html', context)

# ADMIN
@login_required(login_url='login')
def CurrentBookingAdmin(request):
    booking = Booking.objects.filter(booking_status="Confirmed")
    context = {'bookings': booking}
    return render(request, 'rental/admin/current_booking.html', context)

# Driver
@login_required(login_url='login')
def DriverProfile(request):
    driver = Driver.objects.get(user=request.user)
    form = DriverForm(instance=driver)
    if request.method == 'POST':
        form = DriverForm(request.POST, request.FILES, instance=driver)
        if form.is_valid():
            form.save(commit=False).is_first_time = False
            form.save()
            return redirect('driver-dashboard')
    context = {'form': form, 'customer': driver}
    return render(request, 'rental/driver/profile_driver.html', context)

@login_required(login_url='login')
def DriverBookingHistory(request):
    driver = Driver.objects.get(user=request.user)
    booking = Booking.objects.filter(driver=driver).filter(booking_status="Returned")
    context = {'bookings': booking}
    return render(request, 'rental/driver/booking_history.html', context)

@login_required(login_url='login')
def PendingDriverBooking(request):
    driver = Driver.objects.get(user=request.user)
    booking = Booking.objects.filter(driver=driver).filter(booking_status="Pending")
    context = {'bookings': booking}
    return render(request, 'rental/driver/pending_booking.html', context)

# @login_required(login_url='login')
# def CurrentDriverBooking(request):

#     return render(request, 'rental/driver/current_booking.html', context)


@login_required(login_url='login')
def TrackCar(request):
    # booking = Booking.objects.filter(booking_status="Confirmed")
    device_name = "Device 2"
    url = f'https://tracker-a9fe1-default-rtdb.firebaseio.com/locations/{device_name}.json?auth=TRLIkBzUyzxK37fOK2rRTWdjoZjosKEhzPlIMfAa'
    location = requests.get(url) 
    location = location.json()
    lat = location['lat']
    lng = location['lng']
    print(lat)
    print(lng)
    context = {'lat': lat, 'lng': lng}
    return render(request, 'rental/maps.html', context)


# AUTH
def Register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username = form.save()
            user = form.cleaned_data.get('username')
            Customer.objects.create(user=username)
            messages.success(request, f'Account was created for {user}')
            return redirect('login')
    context = {'form': form}
    return render(request, 'rental/register.html', context)

def Login(request):
    if request.user.is_authenticated:
        if request.user.is_customer:
            return redirect('dashboard')
        else:
            return redirect('driver-dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        custominfo = CustomUser.objects.get(username=user)
        if custominfo.is_customer:
            userDet = Customer.objects.get(user=user)
            profile_redirect = 'profile'
        else:
            userDet = Driver.objects.get(user=user)
            profile_redirect = 'driver-profile'
        if user is not None:
            login(request, user)
            if userDet.is_first_time:
                return redirect(profile_redirect)
            else:
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