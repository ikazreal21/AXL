from django.contrib.auth import views as auth_views

from django.urls import path
from . import views




urlpatterns = [
    path("", views.Home, name="home"),
    path("dashboard", views.CustomerDashboard, name="dashboard"),
    path("driver-dashboard", views.DriverDashboard, name="driver-dashboard"),
    path("book/<str:car_id>", views.CustomerBooking, name="book"),
    path("pending-booking", views.PendingBooking, name="pending-booking"),
    path("booking-history", views.BookingHistory, name="booking-history"),
    path("booking-details/<str:booking_id>", views.BookingDetails, name="booking-details"),
    path("confirm-booking/<str:booking_id>", views.ConfirmBooking, name="confirm-booking"),
    path("current-booking", views.CurrentBooking, name="current-booking"),
    path("return-car/<str:booking_id>", views.ReturnCar, name="return-car"),
    # path("calendar", views.Calendar, name="calendar"),


    # AUTH
    path("register/", views.Register, name="register"),
    path("login/", views.Login, name="login"),
    path("logout/", views.Logout, name="logout"),

    # # Download
    # path("download/<str:document_id>", views.download, name="download"),

    # Terms and Conditions
    path("terms-and-conditions", views.TermsAndConditions, name="terms-and-conditions"),
]