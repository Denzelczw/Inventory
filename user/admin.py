from django.contrib import admin
from .models import Profile
from django.contrib.auth.models import User


# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'staff', 'address', 'user_type', 'image']
    list_filter = ['user_type','department']
    search_fields = ['staff__username', 'staff__email', 'address']
    
    list_per_page = 10

