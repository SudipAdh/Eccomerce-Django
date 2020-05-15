
from django.forms import ModelForm

from django.contrib.auth.models import User
from django import forms

from store.models import Product

# from .models import CustomUser


class AddProductForm(ModelForm):
	

	class Meta:
		model = Product
		fields = ["name","price","digital", "image","image1","image2","image3","seller","distance","stock","color","description","size","search_tags"]


