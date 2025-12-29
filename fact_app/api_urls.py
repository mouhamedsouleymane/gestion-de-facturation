from django.urls import path

from . import api

urlpatterns = [
    path('invoices/', api.invoices_list, name='api-invoices-list'),
    path('invoices/<int:pk>/', api.invoice_detail, name='api-invoice-detail'),
    path('customers/', api.customers_list, name='api-customers-list'),
    path('customers/<int:pk>/', api.customer_detail, name='api-customer-detail'),
]
