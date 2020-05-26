from django.contrib import admin

from .models import (
    Product,
    Order,
    OrderItem,
    ShippingAddress,
    OrderDeliveryStatus,
    PaymentInfo,
)


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# from .forms import CustomUserCreationForm, CustomUserChangeForm
# from .models import CustomUser


# class CustomUserAdmin(UserAdmin):
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#     model = CustomUser
#     list_display = [
#         "email",
#         "username",
#     ]


# admin.site.register(CustomUser, CustomUserAdmin)

# admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(OrderDeliveryStatus)
admin.site.register(PaymentInfo)
