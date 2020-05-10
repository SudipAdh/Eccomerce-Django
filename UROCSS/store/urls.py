from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.store, name="store"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("register/", views.registerPage, name="register"),
    path("cart/", views.cart, name="cart"),
    path("checkout", views.Checkout, name="checkout"),
    path("update_item/", views.updateItem, name="update_item"),
    path("process_order/", views.processOrder, name="process_order"),
    path("each_product/<int:pk>/", views.each_product, name="each_product"),
]
