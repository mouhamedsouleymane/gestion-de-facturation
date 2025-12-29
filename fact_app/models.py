from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from decimal import Decimal


class Customer(models.Model):
    """
    Customer model definition
    Stores customer information for invoices
    """
    SEX_TYPES = (
        ('M', _('Male')),
        ('F', _('Feminine')),
    )
    
    name = models.CharField(
        max_length=132,
        help_text="Customer's full name"
    )
    email = models.EmailField(
        unique=True,
        help_text="Customer's email address"
    )
    phone = models.CharField(
        max_length=20,
        help_text="Customer's phone number"
    )
    address = models.CharField(
        max_length=255,
        help_text="Street address"
    )
    sex = models.CharField(
        max_length=1,
        choices=SEX_TYPES,
        help_text="Customer's gender"
    )
    age = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Customer's age"
    )
    city = models.CharField(
        max_length=64,
        help_text="City"
    )
    zip_code = models.CharField(
        max_length=16,
        help_text="Postal code"
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    save_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='customers_created'
    )

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
        ordering = ['-created_date']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['-created_date']),
        ]

    def __str__(self):
        return f"{self.name} ({self.email})"
    
    def get_total_invoices(self):
        """Get total invoice amount for this customer"""
        return sum(inv.get_total for inv in self.invoices.all())
    
    def get_paid_invoices(self):
        """Get all paid invoices for this customer"""
        return self.invoices.filter(paid=True).count()     



class Invoice(models.Model):
    """
    Invoice model definition
    Stores invoice information with related articles
    """

    INVOICE_TYPE = (
        ('R', _('RECEIPT')),
        ('P', _('PROFORMA INVOICE')),
        ('I', _('INVOICE'))
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name='invoices'
    )
    save_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='invoices_created',
        null=True,
        blank=True
    )
    invoice_date_time = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    last_updated_date = models.DateTimeField(null=True, blank=True, auto_now=True)
    paid = models.BooleanField(default=False)
    invoice_type = models.CharField(max_length=1, choices=INVOICE_TYPE, null=True, blank=True)
    comments = models.TextField(null=True, max_length=1000, blank=True)

    class Meta:
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"
        ordering = ['-invoice_date_time']
        indexes = [
            models.Index(fields=['customer']),
            models.Index(fields=['-invoice_date_time']),
            models.Index(fields=['paid']),
        ]

    def __str__(self):
        return f"{self.customer.name} - {self.invoice_date_time.strftime('%Y-%m-%d')} ({self.get_invoice_type_display()})"

    @property
    def get_total(self):
        """Calculate total from related articles"""
        articles = self.articles.all()
        total = sum(Decimal(str(article.get_total)) for article in articles) if articles else Decimal('0.00')
        return total
    
    def mark_as_paid(self):
        """Mark invoice as paid"""
        self.paid = True
        self.save(update_fields=['paid', 'last_updated_date'])
    
    def mark_as_unpaid(self):
        """Mark invoice as unpaid"""
        self.paid = False
        self.save(update_fields=['paid', 'last_updated_date'])
    
    def get_article_count(self):
        """Get number of articles in this invoice"""
        return self.articles.count()    


class Article(models.Model):
    """
    Article model definition
    Stores line items for invoices
    """

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='articles'
    )
    name = models.CharField(
        max_length=255,
        help_text="Product or service name"
    )
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Quantity"
    )
    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Price per unit"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['invoice']),
        ]

    def __str__(self):
        return f"{self.name} (x{self.quantity})"

    @property
    def get_total(self):
        """Calculate total for this line item"""
        return self.quantity * self.unit_price 
        


