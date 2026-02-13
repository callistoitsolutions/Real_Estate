from django.contrib import admin
from django.urls import path
from Vendors import views

urlpatterns = [
      

      ##########urls for Lanlord#####
   
    path('vendors_Dashboard',views.vendors_Dashboard,name="vendors_Dashboard"),
    path('vendor_registration',views.vendor_registration,name="vendor_registration"),
    path('vendor_directory',views.vendor_directory,name="vendor_directory"),
    path('all_links',views.all_links,name="all_links"),
    
    path('register', views.register_vendor, name='register_vendor'),
    path('vendor_filter', views.vendor_filter, name='vendor_filter'),
    path('detail/<int:vendor_id>/', views.vendor_detail, name='vendor_detail'),
    path('vendors/<int:vendor_id>/', views.vendor_profile, name='vendor_profile'),
    path('enquiry/form/', views.enquiry_form, name='enquiry_form'),
    
    path('enquiry/create/', views.create_enquiry, name='create_enquiry'),
    path('enquiry/<str:enquiry_id>/auto_assign/', views.auto_assign_enquiry, name='auto_assign_enquiry'),
    path('enquiry/<str:enquiry_id>/manual_assign/', views.manual_assign_enquiry, name='manual_assign_enquiry'),
    path('enquiry/<str:enquiry_id>/vendor/respond/', views.vendor_respond, name='vendor_respond'),
    path('enquiry/admin/list/', views.admin_enquiry_list, name='admin_enquiry_list'),
    path('enquiry/list/', views.public_enquiry_list, name='public_enquiry_list'),  # optional
    path('enquiry/<str:enquiry_id>/', views.enquiry_detail, name='enquiry_detail'),
    path("dashboard/enquiries/", views.vendor_enquiries, name="vendor_enquiries"),
    path('admin/vendor-performance/', views.admin_vendor_performance, name='admin_vendor_performance'),
    path('admin/vendor/<int:vendor_id>/mark-inhouse/', views.admin_mark_inhouse, name='admin_mark_inhouse'),


]
      
    


   
   


     





