from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, UserUpdateForm, ProfileUpdateForm, StaffProfileUpdateForm, StaffCreationForm
from django.contrib.auth import logout
from django.contrib import messages
from user.models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from .permissions import admin_required, staff_required, head_of_department_required, ict_required

# Create your views here.

@admin_required
def create_staff(request):
    if request.method == 'POST':
        form = StaffCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                messages.success(request, f'Account has been created for {user.get_full_name()} with role: {user.profile.user_type}')
                return redirect('dashboard-staff')
            except IntegrityError:
                messages.error(request, 'A user with this username or email already exists.')
            except Exception as e:
                messages.error(request, f'An error occurred while creating the account: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = StaffCreationForm()
    
    context = {
        'form': form,
        'title': 'Create New Account'
    }
    return render(request, 'user/create_staff.html', context)

@admin_required
def create_user(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create associated profile
            Profile.objects.create(
                staff=user,
                user_type=form.cleaned_data.get('user_type', 'staff')
            )
            # Set user permissions based on user_type
            user_type = form.cleaned_data['user_type'].lower()
            if user_type == 'admin':
                user.is_staff = True
                user.is_superuser = True
            elif user_type in ['staff', 'head_of_department', 'ict']:
                user.is_staff = True
                user.is_superuser = False
            else:
                user.is_staff = False
                user.is_superuser = False
            user.save()
            messages.success(request, f'Account has been created for {user.username}')
            return redirect('dashboard-staff')
    else:
        form = CreateUserForm()
    context = {
        'form': form
    }
    return render(request, 'user/create_user.html', context)

def logout_then_login(request):                             
    logout(request)
    return redirect('user-login')

@login_required
def profile(request):
    return render(request, 'user/profile.html')

@login_required
def profile_update(request, user_id=None):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('user-profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'user/profile_update.html', context)

@admin_required
def staff_profile_update(request, pk=None):
    try:
        staff = Profile.objects.get(pk=pk)
        staff_member = staff.staff
    except Profile.DoesNotExist:
        staff = None 
        staff_member = request.user.profile.staff
    
    if request.method == 'POST':
        profile_form = StaffProfileUpdateForm(request.POST, request.FILES, instance=staff)
        user_form = UserUpdateForm(request.POST, instance=staff_member)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            # Update user permissions based on user_type
            user_type = profile_form.cleaned_data['user_type'].lower()
            if user_type == 'admin':
                staff_member.is_staff = True
                staff_member.is_superuser = True
            elif user_type in ['staff', 'head_of_department', 'ict']:
                staff_member.is_staff = True
                staff_member.is_superuser = False
            else:
                staff_member.is_staff = False
                staff_member.is_superuser = False
            staff_member.save()
            profile_form.save()
            messages.success(request, f'Profile for {staff_member.username} has been updated!')
            return redirect('dashboard-staff')
    else:
        user_form = UserUpdateForm(instance=staff_member)
        profile_form = StaffProfileUpdateForm(instance=staff)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'user/staff_profile_update.html', context)