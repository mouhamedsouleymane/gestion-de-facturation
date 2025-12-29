from django import forms
from django.core.exceptions import ValidationError
from django.forms import formset_factory
from .models import Customer, Invoice, Article


class CustomerForm(forms.ModelForm):
    """
    Form for creating and updating Customer instances
    """
    
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'address', 'sex', 'age', 'city', 'zip_code']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full Name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number',
                'required': True
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Street Address',
                'required': True
            }),
            'sex': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'age': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Age',
                'type': 'number',
                'min': '0',
                'max': '150'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City',
                'required': True
            }),
            'zip_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Postal Code',
                'required': True
            }),
        }

    def clean_email(self):
        """Validate email is unique"""
        email = self.cleaned_data.get('email')
        if email and Customer.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("A customer with this email already exists.")
        return email

    def clean_phone(self):
        """Validate phone format"""
        phone = self.cleaned_data.get('phone')
        if phone and len(phone) < 7:
            raise ValidationError("Phone number must be at least 7 characters long.")
        return phone


class InvoiceForm(forms.ModelForm):
    """
    Form for creating and updating Invoice instances
    """
    
    class Meta:
        model = Invoice
        fields = ['customer', 'invoice_type', 'comments']
        widgets = {
            'customer': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'invoice_type': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'comments': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Additional notes or comments',
                'rows': 4,
                'maxlength': '1000'
            }),
        }


class ArticleForm(forms.ModelForm):
    """
    Form for creating and updating Article instances
    """
    
    class Meta:
        model = Article
        fields = ['name', 'quantity', 'unit_price']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Product/Service Name',
                'required': True
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Quantity',
                'type': 'number',
                'step': '1',
                'min': '1',
                'required': True
            }),
            'unit_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Unit Price',
                'type': 'number',
                'step': '0.01',
                'min': '0',
                'required': True
            }),
        }

    def clean_quantity(self):
        """Validate quantity is positive"""
        quantity = self.cleaned_data.get('quantity')
        if quantity and quantity <= 0:
            raise ValidationError("Quantity must be greater than 0.")
        return quantity

    def clean_unit_price(self):
        """Validate unit price is positive"""
        unit_price = self.cleaned_data.get('unit_price')
        if unit_price and unit_price <= 0:
            raise ValidationError("Unit price must be greater than 0.")
        return unit_price


ArticleFormSet = formset_factory(ArticleForm, extra=1, min_num=1, validate_min=True)
