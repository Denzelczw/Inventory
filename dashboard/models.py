from django.db import models
from django.contrib.auth.models import User
from common.base_model import BaseModel

# Create your models here.

CATERGORY = (
    ('Stationary', 'Stationary'),
    ('Electronics', 'Electronics'),
    ('Food', 'Food'),
)

STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
    ('in_progress', 'In Progress'),
    ('completed', 'Completed'),
)

class Product(BaseModel):
    name = models.CharField(max_length=100, null=True)
    category = models.CharField(max_length=20, choices=CATERGORY, null=True)
    quantity = models.PositiveIntegerField(null=True)

    class Meta:
        verbose_name_plural = 'Product'

    def __str__(self):
        return f'{self.name}-{self.quantity}'

class Order(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    staff = models.ForeignKey(User, models.CASCADE, null=True, related_name='staff_order')
    order_quantity = models.PositiveBigIntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    class Meta:
        verbose_name_plural = 'Order'
        ordering = ['-date']  # Most recent orders first

    def __str__(self):
        return f'{self.product.name} ordered by {self.staff.username}'

class Company(BaseModel):
    name = models.CharField(max_length=100, null=True)
    location = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)

    class Meta:
        verbose_name_plural = 'Company'

    def __str__(self):
        return self.id

class Individual(BaseModel):
    name = models.CharField(max_length=100, null=True)
    registration_number = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=200, null=True)
    location = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)

    class Meta:
        verbose_name_plural = 'Individual'

    def __str__(self):
        return self.id