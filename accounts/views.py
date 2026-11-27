from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            # Automatically log in the newly registered user
            login(request, user)

            return redirect("home")

    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        email = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("home")

        return render(request, "login.html", {
            "error": "Invalid email or password."
        })

    return render(request, "login.html")

@login_required
def home(request):
    return render(request, "home.html")