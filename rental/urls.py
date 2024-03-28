from django.contrib.auth import views as auth_views

from django.urls import path
from . import views




urlpatterns = [
    path("", views.Home, name="home"),
    path("dashboard", views.CustomerDashboard, name="dashboard"),
    path("driver-dashboard", views.DriverDashboard, name="driver-dashboard"),
    # path("calendar", views.Calendar, name="calendar"),


    # AUTH
path("register/", views.Register, name="register"),
    path("login/", views.Login, name="login"),
    path("logout/", views.Logout, name="logout"),

    # # Download
    # path("download/<str:document_id>", views.download, name="download"),
]