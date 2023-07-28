import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Employee(models.Model):
    id = models.CharField(
        max_length=100,
        unique=True,
        default=uuid.uuid4,
        primary_key=True)
    first_name = models.CharField(max_length=50, unique=True, null=True, blank=True)
    last_name = models.CharField(max_length=50, unique=True, null=True, blank=True)
    username= models.CharField(max_length=100, unique=True, null=True, blank=True)
    email = models.EmailField()
    password = models.CharField(max_length=255, null=False, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.first_name}   {self.last_name}'

class Restaurant(models.Model):
    name = models.CharField(unique=True, max_length=255, blank=True, null=True)
    contact = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, null=True, blank=True, on_delete=models.CASCADE)
    file = models.FileField(upload_to='menus/')
    created_by = models.DateField()
    votes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.restaurant.name


class Vote(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.employee}'


