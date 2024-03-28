from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
import locale
import uuid

from django.core.files.storage import FileSystemStorage
from django.db import models

class CustomUser(AbstractUser):
    is_customer = models.BooleanField(default=True, verbose_name='Customer')


class Cars(models.Model):
    car_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    car_name = models.CharField(max_length=255, null=True, blank=True)
    car_model = models.CharField(max_length=255, null=True, blank=True)
    car_license_plate = models.CharField(max_length=255, null=True, blank=True)
    car_price = models.IntegerField()
    car_image = models.ImageField(upload_to='uploads/cars', null=True, blank=True)
    is_available = models.BooleanField(default=True)

    class Meta:  
        verbose_name_plural = 'Cars'
    
    def __str__(self):
        return f"{self.car_name} - {self.car_license_plate}"
    

    
class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    customer_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_name = models.CharField(max_length=255, null=True, blank=True)
    customer_email = models.EmailField(max_length=255, null=True, blank=True)
    customer_phone = models.CharField(max_length=255, null=True, blank=True)
    customer_address = models.CharField(max_length=255, null=True, blank=True)
    customer_license_valid_id = models.ImageField(upload_to='uploads/license', null=True, blank=True)

    def __str__(self):
        return f"{self.customer_name} - {self.customer_email}"
    
class Driver(models.Model):
    driver_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    driver_name = models.CharField(max_length=255, null=True, blank=True)
    driver_email = models.EmailField(max_length=255, null=True, blank=True)
    driver_phone = models.CharField(max_length=255, null=True, blank=True)
    driver_address = models.CharField(max_length=255, null=True, blank=True)
    driver_price = models.IntegerField()
    driver_availability = models.BooleanField(default=True)
    driver_license_valid_id = models.ImageField(upload_to='uploads/license', null=True, blank=True)

    def __str__(self):
        return f"{self.driver_name} - {self.driver_email}"
        

class Booking(models.Model):
    booking_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    car = models.ForeignKey(Cars, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    booking_start_date = models.DateTimeField()
    booking_end_date = models.DateTimeField()
    booking_status = models.CharField(max_length=255, null=True, blank=True)
    toll_fee = models.IntegerField()
    booking_total_price = models.IntegerField()
    is_pickup = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.car} - {self.customer} - {self.driver} - {self.booking_start_date} - {self.booking_end_date} - {self.booking_status} - {self.booking_total_price}"