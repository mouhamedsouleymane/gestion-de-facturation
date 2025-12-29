from django.urls import path
from . import views

app_name = 'fact_app'

urlpatterns = [
    # Invoice URLs
    path('', views.HomeView.as_view(), name='home'),
    path('invoices/<int:pk>/', views.InvoiceDetailView.as_view(), name='view-invoice'),
    path('invoices/<int:pk>/pdf/', views.get_invoice_pdf, name='invoice-pdf'),
    path('invoices/<int:pk>/update-status/', views.UpdateInvoiceStatusView.as_view(), name='update-invoice-status'),
    path('invoices/<int:pk>/delete/', views.DeleteInvoiceView.as_view(), name='delete-invoice'),
    path('invoices/add/', views.AddInvoiceView.as_view(), name='add-invoice'),
    path('invoices/bulk-update-status/', views.bulk_update_invoice_status, name='bulk-update-invoice-status'),
    
    # Customer URLs
    path('customers/', views.CustomerListView.as_view(), name='customer-list'),
    path('customers/add/', views.AddCustomerView.as_view(), name='add-customer'),
    path('customers/<int:pk>/update/', views.UpdateCustomerView.as_view(), name='update-customer'),
    path('customers/<int:pk>/delete/', views.DeleteCustomerView.as_view(), name='delete-customer'),
]