from django import forms
from django.forms import inlineformset_factory
from .models import Stone, Customer, Sale, SaleItem, Supplier, Person

class StoneForm(forms.ModelForm):
    class Meta:
        model = Stone
        fields = ['name', 'stone_type', 'color', 'size', 'unit', 'purchase_price', 'sale_price', 'stock', 'description']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['person', 'customer_code']

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['customer', 'employee']

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['person', 'company_name']

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'national_code', 'phone', 'address', 'person_type']

SaleItemFormSet = inlineformset_factory(
    Sale, 
    SaleItem,
    fields=['stone', 'quantity'],  
    extra=3,                       
    can_delete=True                
)