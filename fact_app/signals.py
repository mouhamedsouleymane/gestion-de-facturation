"""
Django signals for Invoice app
Handles automatic actions when models are saved or deleted
"""
import logging
from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.contrib import messages

from .models import Invoice, Article, Customer

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Article)
def update_invoice_on_article_save(sender, instance, created, **kwargs):
    """
    Update invoice's last_updated_date when an article is saved
    """
    if instance.invoice:
        instance.invoice.save(update_fields=['last_updated_date'])
        logger.debug(f"Invoice {instance.invoice.id} updated after article save")


@receiver(post_delete, sender=Article)
def update_invoice_on_article_delete(sender, instance, **kwargs):
    """
    Update invoice's last_updated_date when an article is deleted
    """
    if instance.invoice:
        instance.invoice.save(update_fields=['last_updated_date'])
        logger.debug(f"Invoice {instance.invoice.id} updated after article delete")


@receiver(post_save, sender=Customer)
def log_customer_creation(sender, instance, created, **kwargs):
    """
    Log customer creation
    """
    if created:
        logger.info(f"New customer created: {instance.name} (ID: {instance.id})")


@receiver(post_save, sender=Invoice)
def log_invoice_creation(sender, instance, created, **kwargs):
    """
    Log invoice creation
    """
    if created:
        logger.info(
            f"New invoice created: Invoice-{instance.id} for {instance.customer.name} "
            f"(Type: {instance.get_invoice_type_display()})"
        )


@receiver(pre_delete, sender=Customer)
def check_customer_invoices(sender, instance, **kwargs):
    """
    Warn if trying to delete customer with invoices
    """
    invoice_count = instance.invoices.count()
    if invoice_count > 0:
        logger.warning(
            f"Customer {instance.name} (ID: {instance.id}) with {invoice_count} invoices "
            f"is being deleted"
        )
