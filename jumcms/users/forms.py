from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .constants import ROLE_CHOICES, BLOOD_GROUP_CHOICES, GENDER_CHOICES
from .models import User


class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirm', widget=forms.PasswordInput)
    role = forms.ChoiceField(choices = ROLE_CHOICES, label = 'Role')
    blood_group = forms.ChoiceField(choices= BLOOD_GROUP_CHOICES, label = 'Blood group')
    gender = forms.ChoiceField(choices = GENDER_CHOICES, label = 'Gender')
    date_of_birth = forms.DateField(label='Date of Birth', widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = User
        fields = [
            "name",
            "email",
            "role",
            "blood_group",
            "date_of_birth",
            "gender",
            "phone_number",
        ]

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ("username", "password")
