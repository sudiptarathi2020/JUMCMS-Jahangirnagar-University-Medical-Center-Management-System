from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.urls import reverse

from .forms import UserRegistrationForm, LoginForm
from .models import Doctor, Patient, Storekeeper, LabTechnician


def home(request):
    """Render the home page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered home page.
    """
    return render(request, "users/home.htm")


def register(request):
    """Handle user registration.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered registration page or a redirect to the unapproved page.
    """
    if request.method == "POST":
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(
                request,
                "Registration successful! Please wait until your account is approved!!",
            )
            return render(request, "users/unapproved.htm")
        else:
            messages.error(request, "Please correct the errors below")
    else:
        form = UserRegistrationForm()

    return render(request, "users/register.html", {"form": form})


def log_in(request):
    """Handle user login.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered login page or a redirect to the home page.
    """
    if request.method == "POST":
        form = LoginForm(data=request.POST)

        if form.is_valid():
            email = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                if user.is_approved:
                    if user.role == "Doctor":
                        Doctor.objects.get_or_create(user=user)
                        return redirect("doctor_dashboard")
                    elif user.role == "Patient":
                        Patient.objects.get_or_create(user=user)
                    elif user.role == "Storekeeper":
                        Storekeeper.objects.get_or_create(user=user)
                        return redirect("storekeeper_dashboard")
                    elif user.role == "LabTechnician":
                        LabTechnician.objects.get_or_create(user=user)
                    return redirect("home")
                else:
                    messages.error(request, "Your account is not approved yet")
                    return render(request, "users/unapproved.htm")
            else:
                form.add_error(None, "Invalid email or password")
                messages.error(request, "Invalid email or password")
                return render(request, "users/login.htm", {"form": form})
        else:
            form.add_error(None, "Invalid email or password")
            messages.error(request, "Invalid email or password")
            return render(request, "users/login.htm", {"form": form})
    else:
        form = LoginForm()

    return render(request, "users/login.htm", {"form": form})


@login_required
def log_out(request):
    """Log the user out and redirect to the home page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: A redirect to the home page after logging out.
    """
    logout(request)
    return redirect("home")


def unapproved(request):
    """Render the unapproved account page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered unapproved page.
    """
    return render(request, "users/unapproved.htm")


# Doctor part start
@login_required
def doctor_dashboard(request):
    doctor = get_object_or_404(Doctor, user=request.user)
    context = {"doctor": doctor}

    return render(request, "doctors/doctor_dashboard.htm", context)


# Doctor part end

# Storekeeper Part Start
@login_required
def storekeeper_dashboard(request):
    user=request.user
    context = {"user": user}
    return render(request, "storekeeper/prescription_search.html", context)

# Storekeeper Part End
