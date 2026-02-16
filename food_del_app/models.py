from django.db import models
from django.contrib.auth.models import AbstractUser
from django.shortcuts import redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings

# Create your models here.
class Foodie(AbstractUser):
    address1 = models.CharField(max_length=100, blank=True, null=True)
    phone_no1 = models.CharField(max_length=20, unique=True, blank=True, null=True)

    # Override existing email field (already present in AbstractUser)
    email = models.EmailField(unique=True)

    # Set email as the unique identifier instead of username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email

    

class Restaurants(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    phone_no = models.CharField(max_length=20)
    image_url = models.ImageField(upload_to='restaurant_imgs/')
    
    
    
    def __str__(self):
        return self.name


class Menus(models.Model):
    restaurant_id = models.ForeignKey(Restaurants,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10,decimal_places=0)
    image_url = models.ImageField(upload_to='menufood_img')


class Orders(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    restaurant_id = models.ForeignKey(Restaurants,on_delete=models.CASCADE)
    order_status = models.CharField(max_length=100)
    order_date = models.DateTimeField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)


class Order_items(models.Model):
    order_id = models.ForeignKey(Orders,on_delete=models.CASCADE)
    menu_item_id = models.ForeignKey(Menus,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(Menus, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.menu_item.name} - {self.quantity} ({self.user.username})"

    def total_price(self):
        return self.menu_item.price * self.quantity
    
    
