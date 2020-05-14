from django.urls import path, re_path
from . import views
from store import views as store_views

urlpatterns = [
    path("", views.backend_login, name="backend_login"),
    path("backend_main/", views.backend_main, name="backend_main"),
    path("add_product_form/", views.add_product_form, name="add_product_form"),
    # path("add_product/", views.add_product, name="add_product"),
]
