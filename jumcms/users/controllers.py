from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import UserRegistrationForm, LoginForm
from .models import Doctor, Patient, Storekeeper, LabTechnician


def home(request):
    return render(request, "users/home.htm")


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return render(request, "users/unapproved.htm")
    else:
        form = UserRegistrationForm()
    return render(request, "users/register.html", {"form": form})


def login(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            email = request.POST["email"]
            password = request.POST["password"]
            # print(email + ":-- " + password)
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                if user.is_authenticated == True:
                    if user.role == "Doctor":
                        Doctor.objects.create(user=user)
                    elif user.role == "Patient":
                        Patient.objects.create(user=user)
                    elif user.role == "Storekeeper":
                        Storekeeper.objects.create(user=user)
                    elif user.role == "LabTechnician":
                        LabTechnician.objects.create(user=user)
                else:
                    return render(request, "users/unapproved.htm")
            return redirect("home")
        else:
            form.add_error(None, "Invalid email or password")
    else:
        form = LoginForm()
    return render(request, "users/login.htm", {"form": form})


@login_required
def log_out(request):
    logout(request)
    return redirect("login")
