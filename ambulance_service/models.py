from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

class Car(models.Model):
    make = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    production_year = models.DateField()
    licence_plate = models.CharField(max_length=7)


class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30,blank=True, null=True)
    last_name = models.CharField(max_length=30,blank=True, null=True)
    phone_number = models.IntegerField(null=True,blank=True)
    national_id = models.IntegerField(null=True,blank=True)
    car_type = models.ForeignKey(Car, on_delete=models.CASCADE, blank=True,null=True)

