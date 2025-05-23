from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

'''We want to add an email on our registration form '''


class CreateUserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        field = '__all__'