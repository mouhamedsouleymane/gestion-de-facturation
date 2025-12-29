import logging
import datetime
from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

import pdfkit

from .models import Customer, Invoice, Article
from .forms import CustomerForm, InvoiceForm, ArticleFormSet
from .utils import pagination, get_invoice
from .decorators import superuser_required

logger = logging.getLogger(__name__)


class SuperuserRequiredMixin(UserPassesTestMixin):
    """Mixin to require superuser status"""
    
    def test_func(self):
        return self.request.user.is_superuser
    
    def handle_no_permission(self):
        messages.error(self.request, _("You do not have permission to access this page."))
        return redirect('admin:login')


class HomeView(LoginRequiredMixin, SuperuserRequiredMixin, ListView):
    """
    Main view - displays list of invoices with pagination
    """
    model = Invoice
    template_name = 'index.html'
    context_object_name = 'invoices'
    paginate_by = 5
    
    def get_queryset(self):
        return Invoice.objects.select_related(
            'customer',
            'save_by'
        ).order_by('-invoice_date_time')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_invoices'] = self.get_queryset().count()
        context['paid_invoices'] = self.get_queryset().filter(paid=True).count()
        return context    



class CustomerListView(LoginRequiredMixin, SuperuserRequiredMixin, ListView):
    """
    View to display list of all customers with pagination
    """
    model = Customer
    template_name = 'customer_list.html'
    context_object_name = 'customers'
    paginate_by = 10
    
    def get_queryset(self):
        return Customer.objects.all().order_by('-created_date')


class AddCustomerView(LoginRequiredMixin, SuperuserRequiredMixin, CreateView):
    """
    Add new customer using CustomerForm
    """
    model = Customer
    form_class = CustomerForm
    template_name = 'add_customer.html'
    success_url = reverse_lazy('customer-list')
    
    def form_valid(self, form):
        """Set the user who creates the customer"""
        form.instance.save_by = self.request.user
        messages.success(
            self.request,
            _("Customer '%(name)s' registered successfully.") % {'name': form.cleaned_data['name']}
        )
        logger.info(f"Customer created: {form.cleaned_data['name']} by {self.request.user}")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Log validation errors"""
        logger.warning(f"Customer creation failed: {form.errors}")
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)


class UpdateCustomerView(LoginRequiredMixin, SuperuserRequiredMixin, UpdateView):
    """
    Update existing customer
    """
    model = Customer
    form_class = CustomerForm
    template_name = 'add_customer.html'
    success_url = reverse_lazy('customer-list')
    
    def form_valid(self, form):
        messages.success(
            self.request,
            _("Customer '%(name)s' updated successfully.") % {'name': form.cleaned_data['name']}
        )
        logger.info(f"Customer updated: {form.cleaned_data['name']} by {self.request.user}")
        return super().form_valid(form)


class DeleteCustomerView(LoginRequiredMixin, SuperuserRequiredMixin, DeleteView):
    """
    Delete a customer
    """
    model = Customer
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('customer-list')
    
    def delete(self, request, *args, **kwargs):
        customer_name = self.get_object().name
        logger.info(f"Customer deleted: {customer_name} by {request.user}")
        messages.success(request, _("Customer deleted successfully."))
        return super().delete(request, *args, **kwargs)   




class AddInvoiceView(LoginRequiredMixin, SuperuserRequiredMixin, CreateView):
    """
    Add new invoice with articles
    """
    model = Invoice
    form_class = InvoiceForm
    template_name = 'add_invoice.html'
    success_url = reverse_lazy('home')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['articles'] = ArticleFormSet(self.request.POST, prefix='articles')
        else:
            context['articles'] = ArticleFormSet(prefix='articles')
        return context
    
    @transaction.atomic()
    def form_valid(self, form):
        """Create invoice and articles atomically"""
        context = self.get_context_data()
        articles = context['articles']
        
        if articles.is_valid():
            form.instance.save_by = self.request.user
            self.object = form.save()
            
            # Create articles
            for article_form in articles:
                if article_form.cleaned_data:
                    article = article_form.save(commit=False)
                    article.invoice = self.object
                    article.save()
            
            messages.success(
                self.request,
                _("Invoice for %(customer)s created successfully with %(count)d items.") % {
                    'customer': form.instance.customer.name,
                    'count': len([a for a in articles if a.cleaned_data])
                }
            )
            logger.info(
                f"Invoice created: ID={self.object.id}, Customer={form.instance.customer.name}, "
                f"by {self.request.user}"
            )
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_invalid(self, form):
        logger.warning(f"Invoice creation failed: {form.errors}")
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)



class InvoiceDetailView(LoginRequiredMixin, SuperuserRequiredMixin, DetailView):
    """
    Display detailed invoice information
    """
    model = Invoice
    template_name = 'invoice.html'
    context_object_name = 'invoice'
    
    def get_queryset(self):
        return Invoice.objects.select_related(
            'customer',
            'save_by'
        ).prefetch_related('articles')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['obj'] = self.object
        context['articles'] = self.object.articles.all()
        return context


class UpdateInvoiceStatusView(LoginRequiredMixin, SuperuserRequiredMixin, UpdateView):
    """
    Update invoice payment status
    """
    model = Invoice
    fields = ['paid', 'comments']
    template_name = 'update_invoice.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        old_paid_status = Invoice.objects.get(pk=self.object.pk).paid
        new_paid_status = form.cleaned_data['paid']
        
        messages.success(
            self.request,
            _("Invoice updated. Status: %(status)s") % {
                'status': _('Paid') if new_paid_status else _('Unpaid')
            }
        )
        logger.info(
            f"Invoice {self.object.id} status changed from {old_paid_status} to {new_paid_status} "
            f"by {self.request.user}"
        )
        return super().form_valid(form)


class DeleteInvoiceView(LoginRequiredMixin, SuperuserRequiredMixin, DeleteView):
    """
    Delete an invoice
    """
    model = Invoice
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('home')
    
    def delete(self, request, *args, **kwargs):
        invoice = self.get_object()
        invoice_info = f"Invoice {invoice.id} for {invoice.customer.name}"
        logger.info(f"Invoice deleted: {invoice_info} by {request.user}")
        messages.success(request, _("Invoice deleted successfully."))
        return super().delete(request, *args, **kwargs)


@login_required
@superuser_required
@require_http_methods(["GET"])
def get_invoice_pdf(request, pk):
    """
    Generate and download PDF for an invoice
    """
    try:
        invoice = get_object_or_404(
            Invoice.objects.select_related(
                'customer',
                'save_by'
            ).prefetch_related('articles'),
            pk=pk
        )
        
        context = {
            'obj': invoice,
            'articles': invoice.articles.all(),
            'date': datetime.datetime.today()
        }
        
        # Get and render template
        template = get_template('invoice-pdf.html')
        html = template.render(context)
        
        # PDF options
        options = {
            'page-size': 'Letter',
            'encoding': 'UTF-8',
            'enable-local-file-access': '',
        }
        
        # Generate PDF
        try:
            pdf = pdfkit.from_string(html, False, options)
        except Exception as e:
            logger.error(f"PDF generation failed for invoice {pk}: {str(e)}")
            messages.error(
                request,
                _("Failed to generate PDF. Please contact support.")
            )
            return redirect('view-invoice', pk=pk)
        
        # Create response
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f"Invoice_{invoice.customer.name}_{invoice.invoice_date_time.strftime('%Y%m%d')}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        logger.info(f"PDF generated for invoice {pk} by {request.user}")
        return response
        
    except Exception as e:
        logger.exception(f"Unexpected error generating PDF for invoice {pk}")
        messages.error(request, _("An error occurred while generating the PDF."))
        return redirect('view-invoice', pk=pk)


@login_required
@require_http_methods(["POST"])
def bulk_update_invoice_status(request):
    """
    Bulk update payment status for multiple invoices
    """
    try:
        invoice_ids = request.POST.getlist('invoice_ids')
        new_status = request.POST.get('status') == 'True'
        
        if not invoice_ids:
            messages.warning(request, _("No invoices selected."))
            return redirect('home')
        
        invoices = Invoice.objects.filter(
            id__in=invoice_ids,
            save_by=request.user
        ) if not request.user.is_superuser else Invoice.objects.filter(id__in=invoice_ids)
        
        updated_count = invoices.update(paid=new_status)
        
        messages.success(
            request,
            _("%(count)d invoice(s) updated successfully.") % {'count': updated_count}
        )
        logger.info(f"Bulk update: {updated_count} invoices status changed to {new_status} by {request.user}")
        
    except Exception as e:
        logger.exception("Error during bulk invoice update")
        messages.error(request, _("An error occurred during bulk update."))
    
    return redirect('home')



