from django.urls import path,include
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'companies', views.CompanyViewSet, basename='company')
router.register(r'individuals', views.IndividualViewSet, basename='individuals')
router.register(r'profiles', views.ProfileViewSet, basename='profiles')


urlpatterns =[
    path('api/',include(router.urls)),
    path('dashboard/', views.index, name = 'dashboard-index'),
    path('staff/pk/', views.staff, name = 'dashboard-staff'),
    path('product/', views.product, name = 'dashboard-product'),    
    path('order/', views.order, name = 'dashboard-order'),
    path('product/delete/<int:pk>', views.product_delete, name = 'dashboard-product-delete'),    
    path('product/update/<int:pk>', views.product_update, name = 'dashboard-product-update'), 
    path('staff/detail/<int:pk>', views.staff_detail, name = 'dashboard-staff-detail'),    
    path('hod/dashboard/', views.hod_dashboard, name='hod_dashboard'),
    path('hod/request/', views.hod_make_request, name='hod-make-request'),
    path('hod/approve-requests/', views.hod_approve_requests, name='hod-approve-requests'),
    path('hod/add-staff/', views.hod_add_staff, name='hod-add-staff'),
    path('hod/manage-staff/', views.hod_manage_staff, name='hod-manage-staff'),
    path('hod/view-requests/', views.hod_view_requests, name='hod-view-requests'),
]