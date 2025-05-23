from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

class CreateUserForm(UserCreationForm):
    email = forms.EmailField()
    user_type = forms.ChoiceField(choices=Profile.user_types)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'user_type']

class StaffCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    address = forms.CharField(max_length=200, required=True)
    user_type = forms.ChoiceField(
        choices=Profile.user_types,
        required=True,
        label='User Role'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'user_type']

    @transaction.atomic
    def save(self, commit=True, created_by_hod=None):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        # Set staff status based on user_type
        user_type = self.cleaned_data['user_type'].lower()
        if user_type == 'admin':
            user.is_staff = True
            user.is_superuser = True
        elif user_type in ['staff', 'head_of_department', 'ict']:
            user.is_staff = True
            user.is_superuser = False
        else:
            user.is_staff = False
            user.is_superuser = False
        
        if commit:
            user.save()
            # Check if profile already exists
            profile, created = Profile.objects.get_or_create(
                staff=user,
                defaults={
                    'user_type': user_type,
                    'address': self.cleaned_data['address'],
                    'created_by_hod': created_by_hod
                }
            )
            if not created:
                # Update existing profile
                profile.user_type = user_type
                profile.address = self.cleaned_data['address']
                if created_by_hod:
                    profile.created_by_hod = created_by_hod
                profile.save()
        return user

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address', 'image']

class StaffProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address', 'image', 'user_type']
    