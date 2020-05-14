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
    context = {}
    return render(request, "backend/backend_main.html", context)


@login_required(login_url="backend_login")
def add_product_form(request):
    form = AddProductForm()

    if request.method == "POST":
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

    context = {"form": form}
    return render(request, "backend/add_product_form.html", context)


# def add_product(request):

#     data = json.loads(request.body)
#     if request.user.is_authenticated and request.user.is_staff:
#         store_models.Product.objects.create(
#             name=data["productInfo"]["product_name"],
#             price=data["productInfo"]["product_price"],
#             digital=string.capwords(data["productInfo"]["product_digital"]),
#             image=data["productInfo"]["product_main_image"],
#             image1=data["productInfo"]["product_image_first"],
#             image2=data["productInfo"]["product_image_second"],
#             image3=data["productInfo"]["product_image_third"],
#             seller=data["productInfo"]["product_seller"],
#             distance=data["productInfo"]["product_distance"],
#             stock=data["productInfo"]["product_stock"],
#             color=data["productInfo"]["product_color"],
#             description=data["productInfo"]["product_description"],
#             size=data["productInfo"]["product_size"],
#             search_tags=data["productInfo"]["product_search_tags"],
#         )

#     else:
#         print("LEAVE THIS")
#     return JsonResponse("Product Added", safe=False)
