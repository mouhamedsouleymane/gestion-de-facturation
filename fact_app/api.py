from __future__ import annotations

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .models import Invoice, Customer


def _invoice_to_dict(inv: Invoice) -> dict:
    return {
        "id": inv.id,
        "customer_id": inv.customer_id,
        "customer_name": inv.customer.name,
        "invoice_date_time": inv.invoice_date_time.isoformat() if inv.invoice_date_time else None,
        "total": str(inv.get_total),
        "paid": inv.paid,
        "invoice_type": inv.invoice_type,
        "invoice_type_display": inv.get_invoice_type_display() if inv.invoice_type else "",
        "comments": inv.comments,
    }


def _customer_to_dict(c: Customer) -> dict:
    return {
        "id": c.id,
        "name": c.name,
        "email": c.email,
        "phone": c.phone,
        "address": c.address,
        "sex": c.sex,
        "age": c.age,
        "city": c.city,
        "zip_code": c.zip_code,
        "created_date": c.created_date.isoformat() if c.created_date else None,
    }


@login_required
@require_http_methods(["GET"])
def invoices_list(request):
    q = (request.GET.get("q") or "").strip()

    qs = Invoice.objects.select_related("customer").order_by("-invoice_date_time")
    if q:
        qs = qs.filter(customer__name__icontains=q) | qs.filter(id__icontains=q)

    data = [_invoice_to_dict(i) for i in qs[:200]]
    return JsonResponse({"results": data})


@login_required
@require_http_methods(["GET"])
def invoice_detail(request, pk: int):
    inv = Invoice.objects.select_related("customer").prefetch_related("articles").get(pk=pk)
    payload = _invoice_to_dict(inv)
    payload["articles"] = [
        {
            "id": a.id,
            "name": a.name,
            "quantity": a.quantity,
            "unit_price": str(a.unit_price),
            "total": str(a.get_total),
        }
        for a in inv.articles.all()
    ]
    return JsonResponse(payload)


@login_required
@require_http_methods(["GET"])
def customers_list(request):
    q = (request.GET.get("q") or "").strip()

    qs = Customer.objects.order_by("-created_date")
    if q:
        qs = qs.filter(name__icontains=q) | qs.filter(email__icontains=q) | qs.filter(phone__icontains=q)

    data = [_customer_to_dict(c) for c in qs[:200]]
    return JsonResponse({"results": data})


@login_required
@require_http_methods(["GET"])
def customer_detail(request, pk: int):
    c = Customer.objects.get(pk=pk)
    return JsonResponse(_customer_to_dict(c))
