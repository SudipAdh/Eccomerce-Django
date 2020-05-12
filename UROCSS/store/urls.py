from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.store, name="store"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("register/", views.registerPage, name="register"),
    re_path(
        r"^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        views.activate,
        name="activate",
    ),
    path("change_password/", views.changePassword, name="change_password"),
    path(
        "reset_password/",
        auth_views.PasswordResetView.as_view(template_name="store/password_reset.html"),
        name="reset_password",
    ),
    path(
        "reset_password_sent/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="store/password_reset_sent.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="store/password_reset_form.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="store/password_reset_done.html"
        ),
        name="password_reset_complete",
    ),
    path("cart/", views.cart, name="cart"),
    path("checkout", views.Checkout, name="checkout"),
    path("update_item/", views.updateItem, name="update_item"),
    path("process_order/", views.processOrder, name="process_order"),
    path("each_product/<int:pk>/", views.each_product, name="each_product"),
    path("search_products/", views.search_products, name="search_products"),
]
# 1->original form submit email form
# 2->success email sent success message
# 3->another form (link to password reset from email)
# 4->success (passowrd succesfully chnaged message)
