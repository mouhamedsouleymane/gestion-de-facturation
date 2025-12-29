from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Customer, Invoice, Article


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """
    Admin interface for Customer model - Modernized with enhanced features
    """
    list_display = ('get_customer_display', 'email', 'phone', 'city', 'get_invoice_count', 'get_total_amount', 'created_date')
    list_filter = ('sex', 'city', 'created_date', 'age')
    search_fields = ('name', 'email', 'phone', 'city', 'address')
    readonly_fields = ('created_date', 'updated_date', 'invoice_stats')
    date_hierarchy = 'created_date'
    ordering = ('-created_date',)
    list_per_page = 25
    
    fieldsets = (
        (_('👤 Personal Information'), {
            'fields': ('name', 'sex', 'age', 'email', 'phone'),
            'description': _('Customer\'s personal details')
        }),
        (_('📋 Address'), {
            'fields': ('address', 'city', 'zip_code'),
            'description': _('Complete customer address')
        }),
        (_('📊 Statistics'), {
            'fields': ('invoice_stats',),
            'classes': ('collapse',)
        }),
        (_('🔧 System Information'), {
            'fields': ('save_by', 'created_date', 'updated_date'),
            'classes': ('collapse',)
        }),
    )
    
    def get_customer_display(self, obj):
        """Display customer with icon and name"""
        icon = '👨' if obj.sex == 'M' else '👩'
        return mark_safe(f'{icon} <strong>{obj.name}</strong>')
    get_customer_display.short_description = _('Customer')
    
    def get_invoice_count(self, obj):
        """Display number of invoices"""
        count = obj.invoices.count()
        color = 'green' if count > 0 else 'gray'
        return format_html(
            '<span style="color: {}; font-weight: bold;">📋 {}</span>',
            color,
            count
        )
    get_invoice_count.short_description = _('Invoices')
    
    def get_total_amount(self, obj):
        """Display total invoice amount"""
        total = obj.get_total_invoices()
        color = 'green' if total > 0 else 'gray'
        return format_html(
            '<span style="color: {}; font-weight: bold;">💰 ${:.2f}</span>',
            color,
            total
        )
    get_total_amount.short_description = _('Total Amount')
    
    def invoice_stats(self, obj):
        """Display invoice statistics"""
        total_invoices = obj.invoices.count()
        paid_invoices = obj.get_paid_invoices()
        total_amount = obj.get_total_invoices()
        
        html = f"""
        <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px;">
            <h3 style="margin-top: 0; color: #333;">📊 Customer Invoice Summary</h3>
            <table style="width: 100%; border-collapse: collapse;">
                <tr style="border-bottom: 1px solid #ddd;">
                    <td style="padding: 8px;"><strong>Total Invoices:</strong></td>
                    <td style="padding: 8px; text-align: right;"><strong>{total_invoices}</strong></td>
                </tr>
                <tr style="border-bottom: 1px solid #ddd;">
                    <td style="padding: 8px;"><strong>Paid Invoices:</strong></td>
                    <td style="padding: 8px; text-align: right; color: green;"><strong>{paid_invoices}</strong></td>
                </tr>
                <tr style="border-bottom: 1px solid #ddd;">
                    <td style="padding: 8px;"><strong>Unpaid Invoices:</strong></td>
                    <td style="padding: 8px; text-align: right; color: red;"><strong>{total_invoices - paid_invoices}</strong></td>
                </tr>
                <tr style="background-color: #e8f5e9;">
                    <td style="padding: 8px;"><strong>Total Amount:</strong></td>
                    <td style="padding: 8px; text-align: right; color: green; font-weight: bold;">💰 ${total_amount:.2f}</td>
                </tr>
            </table>
        </div>
        """
        return mark_safe(html)
    invoice_stats.short_description = _('Invoice Statistics')
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.save_by = request.user
        super().save_model(request, obj, form, change)


class ArticleInline(admin.TabularInline):
    """
    Inline admin for Article model - Enhanced with better formatting
    """
    model = Article
    extra = 1
    fields = ('name', 'quantity', 'unit_price', 'get_total_display', 'created_at')
    readonly_fields = ('get_total_display', 'created_at')
    
    def get_total_display(self, obj):
        """Display formatted total with currency symbol"""
        return format_html(
            '<span style="color: green; font-weight: bold;">💰 ${:.2f}</span>',
            obj.get_total
        )
    get_total_display.short_description = _('Line Total')


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    """
    Admin interface for Invoice model - Modernized with advanced features
    """
    list_display = ('get_invoice_display', 'customer_link', 'invoice_date_time', 'get_total_display', 'get_paid_status', 'invoice_type_badge', 'article_count')
    list_filter = ('paid', 'invoice_type', 'invoice_date_time')
    search_fields = ('customer__name', 'comments', 'id')
    readonly_fields = ('invoice_date_time', 'last_updated_date', 'total_display', 'article_summary')
    inlines = [ArticleInline]
    date_hierarchy = 'invoice_date_time'
    ordering = ('-invoice_date_time',)
    list_per_page = 20
    
    fieldsets = (
        (_('📋 Invoice Information'), {
            'fields': ('customer', 'invoice_type', 'invoice_date_time'),
            'description': _('Basic invoice details')
        }),
        (_('💳 Payment Status'), {
            'fields': ('paid', 'total_display')
        }),
        (_('📝 Additional Information'), {
            'fields': ('comments', 'save_by', 'last_updated_date', 'article_summary'),
            'classes': ('collapse',)
        }),
    )
    
    def get_invoice_display(self, obj):
        """Display invoice with formatted ID"""
        return mark_safe(f'<strong>📄 INV-{obj.id:05d}</strong>')
    get_invoice_display.short_description = _('Invoice')
    
    def customer_link(self, obj):
        """Display clickable customer link"""
        return mark_safe(f'<strong>{obj.customer.name}</strong><br/><small>{obj.customer.email}</small>')
    customer_link.short_description = _('Customer')
    
    def get_total_display(self, obj):
        """Display formatted total with currency symbol"""
        return format_html(
            '<span style="color: green; font-weight: bold; font-size: 14px;">💰 ${:.2f}</span>',
            obj.get_total
        )
    get_total_display.short_description = _('Total')
    
    def get_paid_status(self, obj):
        """Display payment status with color coding"""
        if obj.paid:
            return format_html(
                '<span style="background-color: #c8e6c9; color: #2e7d32; padding: 3px 8px; border-radius: 3px; font-weight: bold;">✓ {}</span>',
                _('Paid')
            )
        return format_html(
            '<span style="background-color: #ffcdd2; color: #c62828; padding: 3px 8px; border-radius: 3px; font-weight: bold;">✗ {}</span>',
            _('Unpaid')
        )
    get_paid_status.short_description = _('Status')
    
    def invoice_type_badge(self, obj):
        """Display invoice type as badge"""
        colors = {
            'R': '#2196F3',  # Receipt - Blue
            'P': '#FF9800',  # Pro-forma - Orange
            'I': '#4CAF50',  # Invoice - Green
        }
        color = colors.get(obj.invoice_type, '#999')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_invoice_type_display()
        )
    invoice_type_badge.short_description = _('Type')
    
    def article_count(self, obj):
        """Display number of articles in invoice"""
        count = obj.articles.count()
        return format_html(
            '<span style="color: #1976D2; font-weight: bold;">🛒 {}</span>',
            count
        )
    article_count.short_description = _('Items')
    
    def total_display(self, obj):
        """Display formatted total in detail view"""
        return format_html(
            '<span style="color: green; font-weight: bold; font-size: 16px;">💰 ${:.2f}</span>',
            obj.get_total
        )
    total_display.short_description = _('Invoice Total')
    
    def article_summary(self, obj):
        """Display summary of articles in invoice"""
        articles = obj.articles.all()
        if not articles:
            return mark_safe('<p style="color: #999;"><em>No articles in this invoice</em></p>')
        
        html = '<table style="width: 100%; border-collapse: collapse;"><tr style="background-color: #f5f5f5;"><th style="padding: 8px; text-align: left;">Product</th><th style="padding: 8px; text-align: right;">Qty</th><th style="padding: 8px; text-align: right;">Price</th><th style="padding: 8px; text-align: right;">Total</th></tr>'
        for article in articles:
            html += f'<tr style="border-bottom: 1px solid #ddd;"><td style="padding: 8px;">{article.name}</td><td style="padding: 8px; text-align: right;">{article.quantity}</td><td style="padding: 8px; text-align: right;">${article.unit_price:.2f}</td><td style="padding: 8px; text-align: right; font-weight: bold; color: green;">${article.get_total:.2f}</td></tr>'
        html += '</table>'
        return mark_safe(html)
    article_summary.short_description = _('Articles Summary')
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.save_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """
    Admin interface for Article model - Modernized interface
    """
    list_display = ('get_name_display', 'get_invoice_link', 'quantity_display', 'price_display', 'get_line_total')
    list_filter = ('created_at', 'invoice__paid', 'invoice__invoice_type')
    search_fields = ('name', 'invoice__customer__name', 'invoice__id')
    readonly_fields = ('created_at', 'line_total_display', 'invoice_summary')
    date_hierarchy = 'created_at'
    list_per_page = 30
    
    fieldsets = (
        (_('📦 Article Information'), {
            'fields': ('invoice', 'name', 'quantity', 'unit_price'),
            'description': _('Product or service details')
        }),
        (_('💰 Totals'), {
            'fields': ('line_total_display', 'invoice_summary'),
            'classes': ('collapse',)
        }),
        (_('🔧 System Information'), {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def get_name_display(self, obj):
        """Display article name with icon"""
        return mark_safe(f'📦 <strong>{obj.name}</strong>')
    get_name_display.short_description = _('Product/Service')
    
    def get_invoice_link(self, obj):
        """Display invoice link with customer info"""
        return mark_safe(f'<strong>INV-{obj.invoice.id:05d}</strong><br/><small>{obj.invoice.customer.name}</small>')
    get_invoice_link.short_description = _('Invoice')
    
    def quantity_display(self, obj):
        """Display quantity"""
        return format_html('<span style="font-weight: bold; font-size: 14px;">{}</span>', obj.quantity)
    quantity_display.short_description = _('Qty')
    
    def price_display(self, obj):
        """Display unit price"""
        return format_html('<span style="color: #1976D2; font-weight: bold;">💰 ${:.2f}</span>', obj.unit_price)
    price_display.short_description = _('Unit Price')
    
    def get_line_total(self, obj):
        """Display line total"""
        return format_html(
            '<span style="color: green; font-weight: bold; font-size: 14px;">💰 ${:.2f}</span>',
            obj.get_total
        )
    get_line_total.short_description = _('Line Total')
    
    def line_total_display(self, obj):
        """Display line total in detail view"""
        return format_html(
            '<span style="color: green; font-weight: bold; font-size: 16px;">💰 ${:.2f}</span>',
            obj.get_total
        )
    line_total_display.short_description = _('Line Total')
    
    def invoice_summary(self, obj):
        """Display invoice summary"""
        invoice = obj.invoice
        html = f"""
        <div style="background-color: #f5f5f5; padding: 10px; border-radius: 5px;">
            <strong>Invoice:</strong> INV-{invoice.id:05d}<br/>
            <strong>Customer:</strong> {invoice.customer.name}<br/>
            <strong>Invoice Total:</strong> <span style="color: green; font-weight: bold;">💰 ${invoice.get_total:.2f}</span><br/>
            <strong>Status:</strong> {'✓ Paid' if invoice.paid else '✗ Unpaid'}
        </div>
        """
        return mark_safe(html)
    invoice_summary.short_description = _('Invoice Summary')

# ============================================================================
# ADMIN SITE CUSTOMIZATION
# ============================================================================

admin.site.site_title = _("Invoice System Admin")
admin.site.site_header = _("📊 Invoice System Administration")
admin.site.index_title = _("Welcome to Invoice System Admin Dashboard")