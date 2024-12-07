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
    date_time = models.DateTimeField()
    quantity = models.CharField(max_length=20)
    location = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=10)
    price_before = models.CharField(max_length=10)
    price_now = models.CharField(max_length=20)


    def __str__(self):
        return  self.product_name


class Worker(models.Model):
    # ForeignKey reference to the User model
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Fields for the worker's information
    name = models.CharField(max_length=50)
    Id_number = models.CharField(max_length=20)
    role = models.CharField(max_length=50)
    mode_payment = models.CharField(max_length=20)
    account = models.CharField(max_length=20)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    # Choices for status and is_active fields
    PENDING = 'Pending'
    ACTIVE = 'Active'
    STATUS_CHOICES = [
        (PENDING, 'Inactive'),
        (ACTIVE, 'Active'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
