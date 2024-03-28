from email.policy import default
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

    def price(self):
        total_amount = float(self.car_price)
        total_amountstr = "{:,.2f}/Day".format(total_amount)
        return total_amountstr
    
    def __str__(self):
        return f"{self.car_name} - {self.car_license_plate}"
    

    
class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    customer_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_name = models.CharField(max_length=255, null=True, blank=True)
    customer_email = models.EmailField(max_length=255, null=True, blank=True)
    customer_phone = models.CharField(max_length=255, null=True, blank=True)
    customer_address = models.CharField(max_length=255, null=True, blank=True)
    customer_license_valid_id = models.ImageField(upload_to='uploads/license', null=True, blank=True)

    def __str__(self):
        return f"{self.customer_name} - {self.customer_email}"
    
class Driver(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    driver_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    driver_name = models.CharField(max_length=255, null=True, blank=True)
    driver_email = models.EmailField(max_length=255, null=True, blank=True)
    driver_phone = models.CharField(max_length=255, null=True, blank=True)
    driver_address = models.CharField(max_length=255, null=True, blank=True)
    driver_price = models.IntegerField()
    driver_availability = models.BooleanField(default=True)
    driver_license_valid_id = models.ImageField(upload_to='uploads/license', null=True, blank=True)

    def price(self):
        total_amount = float(self.driver_price)
        total_amountstr = "{:,.2f}".format(total_amount)
        return total_amountstr

    def __str__(self):
        return f"{self.driver_name} - {self.driver_email}"
        

class Booking(models.Model):

    booking_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    car = models.ForeignKey(Cars, on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True, blank=True)
    booking_start_date = models.DateField()
    booking_end_date = models.DateField()
    booking_status = models.CharField(max_length=255, null=True, blank=True)
    reference_number = models.CharField(max_length=255, null=True, blank=True)
    customer_note = models.TextField(null=True, blank=True)
    customer_license_id = models.ImageField(upload_to='uploads/license', null=True, blank=True)
    customer_valid_id = models.ImageField(upload_to='uploads/valid_id', null=True, blank=True)
    toll_fee = models.IntegerField(default=1000 , null=True, blank=True)
    booking_total_price = models.IntegerField(default=0, null=True, blank=True)
    is_pickup = models.BooleanField(default=False)
    is_cash = models.BooleanField(default=False)

    def price(self):
        if self.booking_total_price:
            total_amount = float(self.booking_total_price)
            total_amountstr = "{:,.2f}".format(total_amount)
            return total_amountstr

    def __str__(self):
        return f"{self.car} - {self.customer} - {self.driver} - {self.booking_start_date} - {self.booking_end_date} - {self.booking_status} - {self.booking_total_price}"