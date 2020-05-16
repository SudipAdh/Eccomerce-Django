from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.forms import inlineformset_factory
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text

# from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.template.loader import render_to_string

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site

from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.contrib.auth.decorators import login_required
import json
import datetime

from .models import *
from .forms import CreateUserForm
from .tokens import account_activation_token


def loginPage(request):
    if request.user.is_authenticated:
        return redirect("store")
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("store")
            else:
                messages.info(request, "Username Or Password is incorrect")

        context = {}
        return render(request, "store/login.html", context)


def logoutUser(request):
    logout(request)
    return redirect("store")


@login_required(login_url="login")
def changePassword(request):
    order = Order.objects.get(customer=request.user, complete=False)
    cartItems = order.get_cart_items
    form = PasswordChangeForm(user=request.user)
    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()

            login(request, form.user)
            return redirect("store")

    context = {"form": form, "cartItems": cartItems}
    return render(request, "store/change_password.html", context)


def registerPage(request):
    if request.user.is_authenticated:
        return redirect("store")
    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)

            if form.is_valid():
                username = request.POST.get("username")
                email = request.POST.get("email")
                password = request.POST.get("password2")
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = "Activate Your URCOSS account."
                message = render_to_string(
                    "store/acc_active_email.html",
                    {
                        "user": user,
                        "domain": current_site.domain,
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "token": account_activation_token.make_token(user),
                    },
                )
                print(user)
                to_email = form.cleaned_data.get("email")
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
                context = {}
                return render(request, "store/signup_email_sent.html", context)
            else:
                context = {"error": form.errors, "form": CreateUserForm()}
                return render(request, "store/register.html", context)

        else:
            context = {"form": form}
            return render(request, "store/register.html", context)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect("login")

    else:
        context = {}
        return render(request, "store/signup_failed.html", context)


def store(request):
    if request.user.is_authenticated:
        # customer = request.user
        try:
            order = Order.objects.get(customer=request.user, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        except:
            order = {"get_cart_items": 0, "get_cart_total": 0, "shipping": False}
            cartItems = order["get_cart_items"]

    else:
        items = []
        order = {"get_cart_items": 0, "get_cart_total": 0, "shipping": False}
        cartItems = order["get_cart_items"]
    products = Product.objects.all().order_by("-created_at")
    context = {"products": products, "cartItems": cartItems}
    return render(request, "store/Store.html", context)


@login_required(login_url="login")
def cart(request):
    if request.user.is_authenticated:
        # customer = request.user
        try:
            order = Order.objects.get(customer=request.user, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        except:
            items = []
            order = {"get_cart_items": 0, "get_cart_total": 0, "shipping": False}
            cartItems = order["get_cart_items"]
    else:
        items = []
        order = {"get_cart_items": 0, "get_cart_total": 0, "shipping": False}
        cartItems = order["get_cart_items"]

    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, "store/Cart.html", context)


@login_required(login_url="login")
def Checkout(request):
    if request.user.is_authenticated:
        # customer = request.user
        try:
            order = Order.objects.get(customer=request.user, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        except:
            items = []
            order = {"get_cart_items": 0, "get_cart_total": 0, "shipping": False}
            cartItems = order["get_cart_items"]

    else:
        items = []
        order = {"get_cart_items": 0, "get_cart_total": 0, "shipping": False}
        cartItems = order["get_cart_items"]
    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, "store/Checkout.html", context)


def updateItem(request):

    data = json.loads(request.body)
    productId = data["productId"]
    action = data["action"]
    print(productId, action)

    # customer = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=request.user, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == "add":
        orderItem.quantity = orderItem.quantity + 1
    elif action == "remove":
        orderItem.quantity = orderItem.quantity - 1
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("Item was added ", safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:

        order = Order.objects.get(customer=request.user, complete=False)

        total = float(data["form"]["total"])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
            order.save()
        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=request.user,
                order=order,
                address=data["shipping"]["address"],
                city=data["shipping"]["city"],
                state=data["shipping"]["state"],
                zipcode=data["shipping"]["zipcode"],
                country=data["shipping"]["country"],
                phone_number=data["shipping"]["phone_number"],
                total=float(data["form"]["total"]),
            )
            OrderDeliveryStatus.objects.create(
                order=order, customer=request.user, address=data["shipping"]["address"]
            )
            PaymentInfo.objects.create(
                order=order, customer=request.user, address=data["shipping"]["address"]
            )

    else:
        print("user is not logged in")
    return JsonResponse("Payment complete", safe=False)


def each_product(request, pk):
    if pk:
        if request.user.is_authenticated:
            try:
                order = Order.objects.get(customer=request.user, complete=False)
                items = order.orderitem_set.all()
                cartItems = order.get_cart_items
            except:
                order = {"get_cart_items": 0, "get_cart_total": 0, "shipping": False}
                cartItems = order["get_cart_items"]
        else:
            order = {"get_cart_items": 0, "get_cart_total": 0, "shipping": False}
            cartItems = order["get_cart_items"]

        product = Product.objects.get(id=pk)

        product = {
            "name": product.name,
            "price": product.price,
            "image": product.imageUrl,
            "image_first": product.image1.url,
            "image_second": product.image2.url,
            "image_third": product.image3.url,
            "seller": product.seller,
            "size": product.size,
            "color": product.color,
            "description": product.description,
            "stock": product.stock,
            "distance": product.distance,
            "id": pk,
        }

    context = {"product": product, "cartItems": cartItems}
    return render(request, "store/view_product.html", context)


def search_products(request):
    if request.method == "GET":
        search_product_name = request.GET.get("search_product_name")
        products = Product.objects.filter(
            search_tags__icontains=search_product_name
        ).order_by("-created_at")

        if request.user.is_authenticated:
            try:
                order = Order.objects.get(customer=request.user, complete=False)
                items = order.orderitem_set.all()
                cartItems = order.get_cart_items
            except:
                order = {"get_cart_items": 0, "get_cart_total": 0, "shipping": False}
                cartItems = order["get_cart_items"]
        else:
            order = {"get_cart_items": 0, "get_cart_total": 0, "shipping": False}
            cartItems = order["get_cart_items"]
        context = {"products": products, "cartItems": cartItems}
        return render(request, "store/Store.html", context)


@login_required(login_url="login")
def order_status(request):
    if request.user.is_authenticated:
        try:
            order_c = Order.objects.get(customer=request.user, complete=False)

            cartItems = order_c.get_cart_items
        except:
            order = {"get_cart_items": 0, "get_cart_total": 0, "shipping": False}
            cartItems = order["get_cart_items"]
    else:
        order_c = {"get_cart_items": 0, "get_cart_total": 0, "shipping": False}
        cartItems = order_c["get_cart_items"]
    orders = Order.objects.filter(customer=request.user, complete=True)

    context = {"orders": orders, "cartItems": cartItems}
    return render(request, "store/order_status.html", context)


@login_required(login_url="login")
def view_order_detail_user(request, id):
    orders = Order.objects.get(transaction_id=id)
    order_items = orders.orderitem_set.all()
    order_delivery_status = orders.orderdeliverystatus_set.all()
    order_payment_status = orders.paymentinfo_set.all()
    if request.user.is_authenticated:
        try:
            order_c = Order.objects.get(customer=request.user, complete=False)

            cartItems = order_c.get_cart_items
        except:
            order = {"get_cart_items": 0, "get_cart_total": 0, "shipping": False}
            cartItems = order["get_cart_items"]
    else:
        order_c = {"get_cart_items": 0, "get_cart_total": 0, "shipping": False}
        cartItems = order_c["get_cart_items"]
    context = {
        "order_items": order_items,
        "order_delivery_statuses": order_delivery_status,
        "order_payment_statuses": order_payment_status,
        "cartItems": cartItems,
    }
    return render(request, "store/order_detail_user.html", context)

