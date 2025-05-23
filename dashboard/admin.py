from django.contrib import admin
from .models import Product, Order, Company, Individual
from django.contrib.auth.models import Group

admin.site.site_header = 'Timb Invetory Dashboard'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'quantity')
    search_fields = ('name', 'category',)
    list_filter = ('category',)
    ordering = ('id',)
    list_per_page = 10

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('product', 'staff', 'order_quantity', 'date', 'status')
    search_fields = ('product__name', 'staff__username')
    list_filter = ('status', 'date')
    list_editable = ('status',)
    date_hierarchy = 'date'
    ordering = ('-date',)
    list_per_page = 10

    @admin.display(description='Product Name')
    def product_name(self, obj):
        return obj.product.name if obj.product else '-'
    @admin.display(description='Staff Name')
    def staff_name(self, obj):
        return obj.staff.username if obj.staff else '-'

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'email', 'phone')
    search_fields = ('name', 'email')

@admin.register(Individual)
class IndividualAdmin(admin.ModelAdmin):
    list_display = ('name', 'registration_number', 'email', 'phone')
    search_fields = ('name', 'email', 'registration_number')
