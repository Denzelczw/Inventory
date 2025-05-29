from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from dashboard.models import Product, Order, Company
from dashboard.serializers import CompanySerializer, IndividualSerializer, ProfileSerializer
from user.models import Profile
from django.contrib.auth.models import User
from .forms import ProductForm, OrderForm
from django.contrib import messages
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from .models import Individual
from user.decorators import hod_required, ict_required
from user.forms import StaffCreationForm

# Create your views here.


@login_required
def index(request):
    if request.user.profile.user_type.lower() == 'head_of_department':
        return redirect('hod_dashboard')
    elif request.user.profile.user_type.lower() == 'ict':
        return redirect('ict_dashboard')
    
    orders = Order.objects.all()
    products = Product.objects.all()
    workers_count = User.objects.all().count()
    order_count = orders.count()
    product_count = products.count()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.staff = request.user
            instance.save()
            return redirect('dashboard-index')
    else:
        form = OrderForm
    context = {
        'orders': orders,
        'form': form,
        'products': products,
        'workers_count': workers_count,
        'orders_count': order_count,
        'product_count': product_count,
    }
    return render(request, 'dashboard/index.html', context)

@login_required
def staff(request,pk=None):
    if pk:
        workers = User.objects.filter(id = pk)
    else:
        workers = User.objects.all()
    workers_count = workers.count()
    orders_count = Order.objects.all().count()
    product_count = Product.objects.all().count()


    context = {
        'workers' : workers,
        'workers_count': workers_count,
        'orders_count': orders_count,
        'product_count': product_count,
    }
    return render(request, 'dashboard/staff.html', context)

@login_required
def staff_detail(request, pk):
    workers = User.objects.get(id = pk)
    context = {
        'workers': workers

    }
    return render(request,'dashboard/staff_detail.html', context)


@login_required
def product(request):
    items = Product.objects.all()                              # Using ORM   Thus is the Read from CRUD
    workers_count = User.objects.all().count()
    product_count = items.count()
    orders_count = Order.objects.all().count()

    if request.method == 'POST':                               # This is where we Create             
        form = ProductForm(request.POST)

        if form.is_valid():
            form.save()
            product_name = form.cleaned_data.get('name')
            messages.success(request, f'{product_name} has been added')
            
            return redirect('dashboard-product')
    else:
        form = ProductForm
    context= {
        'items' : items,
        'form' : form,
        'workers_count': workers_count,
        'product_count': product_count,
        'orders_count': orders_count,
    }
    return render(request, 'dashboard/product.html', context)


# This is where we delete
@login_required
def product_delete(request, pk):
    item = Product.objects.get(id = pk)

    if request.method == 'POST':
        item.delete()
        return redirect('dashboard-product')

    return render(request, 'dashboard/product_delete.html')

# This is where we Update or Edit

@login_required
def product_update(request, pk):
    item = Product.objects.get(id=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance= item)
        if form.is_valid():
            form.save()
            return redirect('dashboard-product')
    else:
        form = ProductForm(instance= item)
    context= {
        'form': form, 

    }
    return render(request, 'dashboard/product_update.html', context) 

@login_required
def order(request):
    orders = Order.objects.all()
    workers_count = User.objects.all().count()
    orders_count = orders.count()
    product_count = Product.objects.all().count()



    context = {
        'orders': orders,
        'workers_count': workers_count,
        'orders_count': orders_count,
        'product_count': product_count,
    }
    return render(request, 'dashboard/order.html', context)

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.AllowAny]

class IndividualViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = IndividualSerializer
    permission_classes = [permissions.AllowAny]


class IndividualViewSet(viewsets.ModelViewSet):
    queryset = Individual.objects.all()
    serializer_class = IndividualSerializer

    def create(self, request, *args, **kwargs):
        # Check if the incoming request is a list of individuals
        if isinstance(request.data, list):
            # Handle bulk creation
            serializer = self.get_serializer(data=request.data, many=True)
            if serializer.is_valid():
                # Bulk create and return the created objects
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # If it's a single object, use the default behavior for creating one individual
            return super().create(request, *args, **kwargs)
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    # Custom action to make an individual an admin
    @action(detail=True, methods=['post'])
    def make_admin(self, request, pk=None):
        try:
            # Get the Profile instance by primary key (pk)
            profile = self.get_object()

            # Ensure the user is not already an admin
            user = profile.staff
            if user.is_superuser:
                return Response({"detail": "User is already an admin."}, status=status.HTTP_400_BAD_REQUEST)

            # Promote the user to an admin
            user.is_superuser = True
            user.is_staff = True  # This makes them able to access the admin panel
            user.save()

            # Update the user_type in the Profile model
            profile.user_type = 'admin'
            profile.save()

            return Response({"detail": f"{user.username} is now an admin."}, status=status.HTTP_200_OK)

        except Profile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

@login_required
@hod_required
def hod_dashboard(request):
    department = request.user.profile.department
    # Get all staff members created by this HOD
    staff_members = User.objects.filter(
        profile__created_by_hod=request.user,
        profile__user_type='staff'
    ).select_related('profile').order_by('-date_joined')

    # Only count pending requests from staff created by this HOD
    pending_requests = Order.objects.filter(
        staff__profile__created_by_hod=request.user,
        status='pending'
    )

    context = {
        'staff_members': staff_members,
        'staff_count': staff_members.count(),
        'pending_count': pending_requests.count(),
        'pending_approvals_count': pending_requests.count(),
    }
    return render(request, 'Dashboard/HOD/index.html', context)

@login_required
@hod_required
def hod_make_request(request):
    department = request.user.profile.department
    pending_approvals_count = Order.objects.filter(staff__profile__department=department, status='pending').count()
    my_orders = Order.objects.filter(staff=request.user).order_by('-created_at')
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.staff = request.user
            instance.save()
            messages.success(request, 'Your request has been submitted successfully.')
            form = OrderForm()  # Reset the form after successful submission
            # Do not redirect; stay on the page
    else:
        form = OrderForm
    return render(request, 'Dashboard/HOD/make_request.html', {
        'form': form,
        'pending_approvals_count': pending_approvals_count,
        'my_orders': my_orders,
    })

@login_required
@hod_required
def hod_approve_requests(request):
    department = request.user.profile.department
    pending_requests = Order.objects.filter(staff__profile__department=department, status='pending')
    pending_approvals_count = pending_requests.count()
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        action = request.POST.get('action')
        order = Order.objects.get(id=order_id)
        if action == 'approve':
            order.status = 'approved'
        elif action == 'reject':
            order.status = 'rejected'
        order.save()
        return redirect('hod-approve-requests')
    return render(request, 'hod/approve_requests.html', {'pending_requests': pending_requests, 'pending_approvals_count': pending_approvals_count})

@login_required
@hod_required
def hod_add_staff(request):
    department = request.user.profile.department
    pending_approvals_count = Order.objects.filter(staff__profile__department=department, status='pending').count()
    if request.method == 'POST':
        form = StaffCreationForm(request.POST)
        if form.is_valid():
            user = form.save(created_by_hod=request.user)
            messages.success(request, f'Staff account created for {user.get_full_name()}')
            form = StaffCreationForm()  # Reset form after success
    else:
        form = StaffCreationForm()
    return render(request, 'Dashboard/HOD/add_staff.html', {
        'form': form,
        'pending_approvals_count': pending_approvals_count,
    })

@login_required
@hod_required
def hod_manage_staff(request):
    department = request.user.profile.department
    staff = User.objects.filter(profile__department=department, profile__user_type='staff')
    pending_approvals_count = Order.objects.filter(staff__profile__department=department, status='pending').count()
    return render(request, 'hod/manage_staff.html', {'staff': staff, 'pending_approvals_count': pending_approvals_count})

@login_required
@hod_required
def hod_my_requests(request):
    my_orders = Order.objects.filter(staff=request.user)
    return render(request, 'hod/my_requests.html', {'my_orders': my_orders})

@login_required
@hod_required
def hod_view_requests(request):
    # Get all requests from staff members created by this HOD
    requests = Order.objects.filter(
        staff__profile__created_by_hod=request.user
    ).select_related('staff', 'product').order_by('-created_at')
    
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        action = request.POST.get('action')
        
        try:
            order = Order.objects.get(id=order_id, staff__profile__created_by_hod=request.user)
            if action == 'approve':
                order.status = 'approved'
                messages.success(request, f'Request for {order.product.name} has been approved.')
            elif action == 'reject':
                order.status = 'rejected'
                messages.warning(request, f'Request for {order.product.name} has been rejected.')
            order.save()
        except Order.DoesNotExist:
            messages.error(request, 'Request not found or you do not have permission to modify it.')
        
        return redirect('hod-view-requests')
    
    context = {
        'requests': requests,
        'pending_approvals_count': requests.filter(status='pending').count(),
    }
    return render(request, 'Dashboard/HOD/view_requests.html', context)
