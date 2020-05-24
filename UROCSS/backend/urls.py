from django.urls import path
from . import views


urlpatterns = [
    path("", views.backend_login, name="backend_login"),
    path("backend_logout", views.backend_logout, name="backend_logout"),
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
    path(
        "view_product_in_table/",
        views.view_product_in_table,
        name="view_product_in_table",
    ),
    path(
        "edit_product_form/<str:id>/",
        views.edit_product_form,
        name="edit_product_form",
    ),
    path("delete_product/", views.delete_product, name="delete_product"),
    path(
        "set_product_detail/<str:id>/",
        views.set_product_detail,
        name="set_product_detail",
    ),
    path(
        "out_of_stock_product/",
        views.out_of_stock_product,
        name="out_of_stock_product",
    ),
    path("new_orders/", views.new_orders, name="new_orders"),
    path("confirmed_orders/", views.confirmed_orders, name="confirmed_orders"),
    path("delivered_orders/", views.delivered_orders, name="delivered_orders"),
    path("paid_orders/", views.paid_orders, name="paid_orders"),
]
