
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import uuid


class CustomUser(AbstractUser):
   address = models.TextField(blank=True, null=True)# Ensure this exists
   phonenumber = models.CharField(max_length=15, blank=True, null=True)  # Add this field  
   

def __str__(self):
        return self.username
   

   


class Vegetable(models.Model):
    CATEGORY_CHOICES = [
        ('vegetable', 'Vegetable'),
        ('leafy', 'Leafy Vegetable'),
    ]

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    weight = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to='vegetables/', blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='vegetable')
    quantity = models.PositiveIntegerField(default=1)
    def __str__(self):
        return self.name

 
class Cart(models.Model):
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, )
    vegetable = models.ForeignKey(Vegetable, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.vegetable.price * self.quantity

    


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Address Model
class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="addresses")
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10)
    country = models.CharField(max_length=100)

    def _str_(self):
        return f"{self.street_address}, {self.city}, {self.state} - {self.zipcode}"


# Order Model
class Order(models.Model):
    STATUS_CHOICES = [
        ('Processing', 'Processing'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Shipped', 'Shipped')
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Processing')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2,default=0)

    def _str_(self):
        return f"Order {self.id} by {self.user}"
    

# OrderItem Model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    vegetable = models.ForeignKey(Vegetable, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def _str_(self):
        return f"{self.quantity} x {self.vegetable.name}"
    


