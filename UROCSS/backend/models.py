from django.db import models

from phone_field import PhoneField


class Seller(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField(blank=True)
    shop_name = models.CharField(max_length=200)
    shop_address = models.CharField(max_length=200)
    contact_number = PhoneField(blank=True)

    def __str__(self):
        return self.name
