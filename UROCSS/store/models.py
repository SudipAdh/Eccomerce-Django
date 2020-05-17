from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):

    name = models.CharField(max_length=200)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    image1 = models.ImageField(null=True, blank=True)
    image2 = models.ImageField(null=True, blank=True)
    image3 = models.ImageField(null=True, blank=True)
    seller = models.CharField(max_length=100, null=True)
    distance = models.CharField(max_length=5, null=True)
    stock = models.IntegerField(default=0)
    color = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=200, null=True)
    size = models.CharField(max_length=100, null=True)
    search_tags = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def imageUrl(self):
        try:
            url = self.image.url

        except Exception:
            url = ""
        return url


class Order(models.Model):
    customer = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True
    )
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        if self.transaction_id is not None:
            return str(
                self.transaction_id + "(" + str(self.date_ordered) + ")"
            )
        else:
            return str(self.transaction_id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if not i.product.digital:
                shipping = True

        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, blank=True, null=True
    )
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, blank=True, null=True
    )
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    def __str__(self):
        return str(self.order)


class ShippingAddress(models.Model):
    customer = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True
    )
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, blank=True, null=True
    )
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=40, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=10, null=True)
    total = models.IntegerField(default=0)

    def __str__(self):
        return str(self.order)


class OrderDeliveryStatus(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, blank=True, null=True
    )
    customer = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True
    )
    address = models.CharField(max_length=200, null=True)
    confirmed = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)

    def __str__(self):
        if self.confirmed and self.delivered:
            return str("Confirmed and Delivered= True | " + str(self.order))
        elif self.confirmed and self.delivered:
            return str(
                "Confirmed True and Delivered False | " + str(self.order)
            )
        elif not self.confirmed and not self.delivered:
            return str("New Order | " + str(self.order))
        else:
            return str("Not Possible Plz chech status")


class PaymentInfo(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, blank=True, null=True
    )
    customer = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True
    )
    address = models.CharField(max_length=200, null=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        if not self.paid:
            return str("New Order Not Paid | " + str(self.order))
        else:
            return str("Paid | " + str(self.order))
