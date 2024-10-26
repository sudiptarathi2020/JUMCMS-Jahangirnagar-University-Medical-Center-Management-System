from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import UserRegistrationForm, LoginForm
from .models import Doctor, Patient, Storekeeper, LabTechnician


# Create your views here.

def home(request):
    return render(request, "users/home.htm")

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            role = form.cleaned_data['role']
            user.save()

            if role == 'Doctor':
                Doctor.objects.create(user=user)
            elif role == 'Patient':
                Patient.objects.create(user=user)
            elif role == 'Storekeeper':
                Storekeeper.objects.create(user=user)
            elif role == 'LabTechnician':
                LabTechnician.objects.create(user=user)

            log_in(request)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def log_in(request):
    if request.method == 'POST':
        form = LoginForm(request, data= request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request,user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def log_out(request):
    logout(request)
    return redirect('login')
