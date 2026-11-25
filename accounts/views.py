from django.shortcuts import render
from django.contrib.auth import login
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import RegisterForm


def register(request):
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("home")
    return render(request, "register.html", {"form": form})


def home(request):
    return HttpResponse("Welcome! Account created.")