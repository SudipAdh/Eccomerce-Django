from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse


from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from store import models as store_models

import json

from .forms import AddProductForm
import string


def backend_login(request):
    if request.user.is_authenticated and request.user.is_staff == True:
        return redirect("backend_main")

        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None and user.is_staff == True:
                login(request, user)
                return redirect("backend_main")
            else:
                messages.info(
                    request,
                    "You don't have staff access ! Please leave this page or else legal action will be taken.",
                )

        context = {}
        return render(request, "backend/backend_login.html", context)

    elif request.user.is_authenticated and request.user.is_staff == False:
        return HttpResponse(
            "<h1>Dear Customer, you dont have Authority to access this page</h1>"
        )
    else:
        return HttpResponse(
            "<h1>Please leave this page or else legal action will be taken.</h1>"
        )


@login_required(login_url="backend_login")
def backend_main(request):
    orders = store_models.Order.objects.all()

    context = {"orders": orders}
    return render(request, "backend/backend_main.html", context)


@login_required(login_url="backend_login")
def add_product_form(request):
    form_clear = AddProductForm()

    if request.method == "POST":
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            context = {"form": form_clear}
            return render(request, "backend/add_product_form.html", context)

    context = {"form": form_clear}
    return render(request, "backend/add_product_form.html", context)


@login_required(login_url="backend_login")
def view_order_detail(request, id):
    id = float(id)
    order = store_models.Order.objects.get(transaction_id=id)
    order_items = order.orderitem_set.all()
    shipping_info = order.shippingaddress_set.all()
    order_delivery_status_data = order.orderdeliverystatus_set.all()
    order_payment_status_data = order.paymentinfo_set.all()
    context = {
        "order_items": order_items,
        "shipping_infos": shipping_info,
        "order_delivery_statuses": order_delivery_status_data,
        "transaction_id": str(id),
        "order_payment_statuses": order_payment_status_data,
    }
    return render(request, "backend/view_order_detail.html", context)


@login_required(login_url="backend_login")
def order_delivery_status(request, id):
    if request.method == "POST":
        id = float(id)
        confirm = request.POST["confirm"]
        deliver = request.POST["deliver"]
        payment = request.POST["payment"]
        order = store_models.Order.objects.get(transaction_id=id)
        order_items = order.orderitem_set.all()
        shipping_info = order.shippingaddress_set.all()
        order_delivery_status_data = order.orderdeliverystatus_set.all()
        order_payment_status_data = order.paymentinfo_set.all()
        order_delivery_status_data.update(confirmed=confirm, delivered=deliver)
        order_payment_status_data.update(paid=payment)
        context = {
            "order_items": order_items,
            "shipping_infos": shipping_info,
            "order_delivery_statuses": order_delivery_status_data,
            "transaction_id": str(id),
            "order_payment_statuses": order_payment_status_data,
        }
        return render(request, "backend/view_order_detail.html", context)
