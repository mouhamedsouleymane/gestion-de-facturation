"""
Utility functions for invoice and customer management
"""
import logging
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Invoice, Customer

logger = logging.getLogger(__name__)


def pagination(request, queryset, items_per_page=5):
    """
    Paginate a queryset based on the request's page parameter.
    
    Args:
        request: Django request object
        queryset: QuerySet to paginate
        items_per_page: Number of items per page (default: 5)
    
    Returns:
        Page object containing paginated items
    """
    default_page = 1
    page = request.GET.get('page', default_page)
    
    try:
        paginator = Paginator(queryset, items_per_page)
        items_page = paginator.page(page)
    except PageNotAnInteger:
        items_page = paginator.page(default_page)
    except EmptyPage:
        items_page = paginator.page(paginator.num_pages)
    
    return items_page


def get_invoice(pk):
    """
    Retrieve invoice with all related articles.
    
    Args:
        pk: Invoice primary key
    
    Returns:
        Dictionary containing invoice and articles
    
    Raises:
        Invoice.DoesNotExist: If invoice not found
    """
    try:
        invoice = Invoice.objects.select_related(
            'customer',
            'save_by'
        ).prefetch_related('articles').get(pk=pk)
        
        context = {
            'obj': invoice,
            'articles': invoice.articles.all(),
            'total': invoice.get_total,
        }
        
        logger.debug(f"Retrieved invoice {pk} with {invoice.articles.count()} articles")
        return context
        
    except Invoice.DoesNotExist:
        logger.warning(f"Invoice {pk} not found")
        raise


def get_customer_summary(customer_id):
    """
    Get comprehensive summary for a customer including invoice statistics.
    
    Args:
        customer_id: Customer primary key
    
    Returns:
        Dictionary with customer summary data
    """
    try:
        customer = Customer.objects.select_related('save_by').get(pk=customer_id)
        invoices = customer.invoices.all()
        
        total_invoices = invoices.count()
        paid_invoices = invoices.filter(paid=True).count()
        total_amount = sum(inv.get_total for inv in invoices)
        
        context = {
            'customer': customer,
            'total_invoices': total_invoices,
            'paid_invoices': paid_invoices,
            'unpaid_invoices': total_invoices - paid_invoices,
            'total_amount': total_amount,
        }
        
        return context
        
    except Customer.DoesNotExist:
        logger.warning(f"Customer {customer_id} not found")
        raise


def get_invoice_statistics(start_date=None, end_date=None):
    """
    Get invoice statistics for a date range.
    
    Args:
        start_date: Start date for filtering (optional)
        end_date: End date for filtering (optional)
    
    Returns:
        Dictionary with invoice statistics
    """
    queryset = Invoice.objects.all()
    
    if start_date:
        queryset = queryset.filter(invoice_date_time__gte=start_date)
    
    if end_date:
        queryset = queryset.filter(invoice_date_time__lte=end_date)
    
    total_invoices = queryset.count()
    paid_invoices = queryset.filter(paid=True).count()
    total_amount = sum(inv.get_total for inv in queryset)
    
    return {
        'total_invoices': total_invoices,
        'paid_invoices': paid_invoices,
        'unpaid_invoices': total_invoices - paid_invoices,
        'total_amount': total_amount,
        'average_invoice': total_amount / total_invoices if total_invoices > 0 else 0,
    }