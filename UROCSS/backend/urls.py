from django.urls import path, re_path
from . import views
from store import views as store_views

urlpatterns = [
    path("", views.backend_login, name="backend_login"),
    path("backend_main/", views.backend_main, name="backend_main"),
    path("add_product_form/", views.add_product_form, name="add_product_form"),
    path(
        "view_order_detail/<str:id>/",
        views.view_order_detail,
        name="view_order_detail",
    ),
    path(
        "order_delivery_status/<str:id>",
        views.order_delivery_status,
        name="order_delivery_status",
    ),
]
