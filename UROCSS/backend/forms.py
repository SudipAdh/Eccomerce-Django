
from django.forms import ModelForm

from store.models import Product
from .models import Seller

# from .models import CustomUser


class AddProductForm(ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "price",
            "digital",
            "image",
            "image1",
            "image2",
            "image3",
            "seller",
            "distance",
            "stock",
            "color",
            "description",
            "size",
            "search_tags",
        ]


class AddSellerForm(ModelForm):
    class Meta:
        model = Seller
        fields = [
            "name",
            "age",
            "shop_name",
            "shop_address",
            "contact_number"
        ]