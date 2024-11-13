from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm, LoginForm
from .models import Doctor, Patient, Storekeeper, LabTechnician
from appointments.controllers import get_doctor_appointments
from django.utils import timezone
from collections import defaultdict


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

    This function processes registration requests, validates the user input,
    and saves the new user if valid. If the registration is successful,
    it redirects the user to the unapproved page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered registration page or a redirect to the
            unapproved page.
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

    This function processes login requests and authenticates the user. If
    the login is successful and the user's account is approved, the user
    is redirected to their respective dashboard based on their role.

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
                        return redirect("doctor-dashboard")
                    elif user.role == "Student":
                        Patient.objects.get_or_create(user=user)
                    elif user.role == "Campus_employee":
                        Patient.objects.get_or_create(user=user)
                    elif user.role == "Storekeeper":
                        Storekeeper.objects.get_or_create(user=user)
                    elif user.role == "Lab_technician":
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

    This page informs users that their accounts are pending approval.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered unapproved page.
    """
    return render(request, "users/unapproved.html")


@login_required
def doctor_dashboard(request):
    """Render the doctor's dashboard.

    This function retrieves the doctor's appointments for the current day
    and aggregates the appointments per month for display in the dashboard.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered doctor dashboard page with the doctor's
            information and appointments data.
    """
    doctor = get_object_or_404(Doctor, user=request.user)
    appointments_list = get_doctor_appointments(doctor)
    today = timezone.now().date()
    appointments_today = [
        appointment
        for appointment in appointments_list
        if appointment.appointment_date_time.date() == today
    ]

    appointments_per_month = defaultdict(int)

    for appointment in appointments_list:
        appointment_year = appointment.appointment_date_time.year
        appointment_month = appointment.appointment_date_time.month
        if appointment_year == today.year:
            appointments_per_month[appointment_month] += 1

    appointments_data = [appointments_per_month[i] for i in range(1, 13)]
    context = {
        "doctor": doctor,
        "appointments_list": appointments_list,
        "today": today,
        "appointments_today": appointments_today,
        "appointments_data": appointments_data,
    }
    return render(request, "doctors/doctor_dashboard.htm", context)
