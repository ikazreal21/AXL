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
    path("late-return", views.LateReturnBooking, name="late-return"),
    path("booking-details/<str:booking_id>", views.BookingDetails, name="booking-details"),
    path("confirm-booking/<str:booking_id>", views.ConfirmBooking, name="confirm-booking"),
    path("current-booking", views.CurrentBooking, name="current-booking"),
    path("return-car/<str:booking_id>", views.ReturnCar, name="return-car"),
    path("biling/<str:booking_id>", views.Billing, name="billing"),
    path("cancel-booking/<str:booking_id>", views.CancelBooking, name="cancel-booking"),
    path("invoice/<str:booking_id>", views.Invoice, name="invoice"),
    path("profile", views.CustomerProfile, name="profile"),
    # path("calendar", views.Calendar, name="calendar"),


    # AUTH
    path("register/", views.Register, name="register"),
    path("login/", views.Login, name="login"),
    path("logout/", views.Logout, name="logout"),

    # # Download
    # path("download/<str:document_id>", views.download, name="download"),

    # Terms and Conditions
    path("terms-and-conditions", views.TermsAndConditions, name="terms-and-conditions"),

    # Maps
    path("tracker", views.TrackCar, name="tracker"),
]