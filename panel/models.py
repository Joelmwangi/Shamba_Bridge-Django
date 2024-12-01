from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings



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
    phone_number = models.CharField(max_length=20)
    price_before = models.CharField(max_length=10)
    price_now = models.CharField(max_length=20)


def send_welcome_email(user_email):
    subject = 'Welcome to Our Platform'
    message = 'Thank you for registering on our platform. We are excited to have you!'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

    def __str__(self):
        return  self.product_name

class Worker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    Id_number = models.CharField(max_length=20)
    role = models.CharField(max_length=50)
    mode_payment = models.CharField(max_length=20)
    account = models.CharField(max_length=20)
    phone = models.CharField(max_length=30)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive')])
    status_salary = models.CharField(max_length=20, default="Pending")

    def __str__(self):
        return self.name