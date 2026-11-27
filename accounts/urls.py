from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        auth_views.LoginView.as_view(template_name="login.html"),
        name="login",
    ),
    path("home/", views.home, name="home"),
    path("register/", views.register, name="register"),

]