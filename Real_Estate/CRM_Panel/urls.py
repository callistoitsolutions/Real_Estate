from django.contrib import admin
from django.urls import path
from CRM_Panel import views

urlpatterns = [
      

      ##########urls for Lanlord#####
   
    ## path('auto_capture',views.auto_capture,name="auto_capture"),
     path('crm_dashboard',views.crm_dashboard,name="crm_dashboard"),
     #path('manual_entry',views.manual_entry,name="manual_entry"),
     #path('Lead_Status_Update_crm',views.Lead_Status_Update_crm,name="Lead_Status_Update_crm"),
     path('Lead_Assignment_crm',views.Lead_Assignment_crm,name="Lead_Assignment_crm"),
    # path('Lead_Age_Analysis',views.Lead_Age_Analysis,name="Lead_Age_Analysis"),
    # path('Wallet_Transaction',views.Wallet_Transaction,name="Wallet_Transaction"),
    # path('Wallet_Recharge',views.Wallet_Recharge,name="Wallet_Recharge"),
     #path('Lead_Buy_Request',views.Lead_Buy_Request,name="Lead_Buy_Request"),
     path('Lead_History',views.Lead_History,name="Lead_History"),
     path('Bulk_Lead_Upload',views.Bulk_Lead_Upload,name="Bulk_Lead_Upload"),
     
     path('auto-lead/new/', views.auto_lead_create, name='auto_lead_create'),
     path('auto-lead/', views.auto_lead_list, name='auto_lead_list'),
     path('auto-lead/edit/<int:pk>/', views.auto_lead_edit, name='auto_lead_edit'),
     path('auto-lead/<int:pk>/delete/', views.auto_lead_delete, name='auto_lead_delete'),
     
     path("manual-lead/new/", views.manual_lead_create, name="manual_lead_create"),
     path("manual-lead/", views.manual_lead_list, name="manual_lead_list"),
     
     path("lead-status/new/", views.lead_status_create, name="lead_status_create"),
     path("lead-status/", views.lead_status_list, name="lead_status_list"),
     
 

     path("lead-age-analysis/new/", views.lead_age_analysis_create, name="lead_age_analysis_create"),
     path("lead-age-analysis/", views.lead_age_analysis_list, name="lead_age_analysis_list"),
     
  
     path("wallet-transaction/new/", views.wallet_transaction_create, name="wallet_transaction_create"),
     path("wallet-transaction/", views.wallet_transaction_list, name="wallet_transaction_list"),
     
  
     path("wallet-recharge/new/", views.wallet_recharge_create, name="wallet_recharge_create"),
     path("wallet-recharge/", views.wallet_recharge_list, name="wallet_recharge_list"),
     

     path("lead-buy-request/new/", views.lead_buy_request_create, name="lead_buy_request_create"),
     path("lead-buy-request/", views.lead_buy_request_list, name="lead_buy_request_list"),
     
     #path('crm/assignees/', views.assignees_list, name='assignees_list'),
    # path('crm/assign-lead/', views.assign_lead, name='assign_lead'),
   
     
 


     
]










    
    # Repeat pattern for all other forms, e.g.
    # path('manual-lead/new/', views.manual_lead_create, name='manual_lead_create'),
    # path('manual-lead/', views.manual_lead_list, name='manual_lead_list'), ...

   
     
    








