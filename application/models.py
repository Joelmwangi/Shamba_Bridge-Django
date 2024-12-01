from unicodedata import decimal
from django.db import models


class Order(models.Model):
    product_name = models.CharField(max_length=255)
    price_now = models.DecimalField(max_digits=10, decimal_places=2)
    payment_number = models.CharField(max_length=20)

    def __str__(self):
        return self.product_name