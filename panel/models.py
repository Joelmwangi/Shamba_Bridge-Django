from django.db import models
from django.contrib.auth.models import User



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/', blank=True)
    name = models.CharField(max_length=20)
    farm_nol = models.CharField(max_length=20, blank=True)
    farm_product = models.CharField(max_length=30)
    location = models.CharField(max_length=20)

    def __str__(self):
        return  self.name

class Product(models.Model):
   # user = models.OneToOneField(User, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='products_images/', blank=True)
    date_time = models.DateField()
    price_before = models.CharField(max_length=10)
    location = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=10)
    price_now = models.CharField(max_length=20)


    def __str__(self):
        return  self.product_name