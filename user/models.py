from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

# Create your models here.

class Profile(models.Model):
    user_types = (
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('head_of_department', 'HOD'),
        ('ict', 'ICT'),
    )
    staff = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='profile')
    address = models.CharField(max_length=200, null=True)
    user_type = models.CharField(max_length=20, choices=user_types, default='staff')
    image = models.ImageField(default='avatar.jpg', upload_to='Profile_Images')
    department = models.CharField(max_length=100, null=True, blank=True)
    created_by_hod = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='hod_created_staff')

    def __str__(self):
        return f'{self.staff.username}-Profile'
    
    @property
    def get_staff_orders(self):
        return self.staff.staff_order.all()