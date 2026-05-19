from django import forms

from .models import *


class StoneForm(forms.ModelForm):
    class Meta:
        model = Stone
        fields = [
            'name',
            'stone_type',
            'color',
            'size',
            'unit',
            'purchase_price',
            'sale_price',
            'stock',
            'description'
        ]
from django import forms
from .models import Customer


class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ['person', 'customer_code']

class PurchaseForm(forms.ModelForm):

    class Meta:
        model = Purchase
        fields = ['supplier', 'employee','purchasitem']
class SaleForm(forms.ModelForm):

    class Meta:
        model = Sale
        fields = ['customer', 'employee']
class PurchaseItemForm(forms.ModelForm):

    class Meta:
        model = PurchaseItem
        fields = ['stone', 'quantity']
class SaleItemForm(forms.ModelForm):

    class Meta:
        model = SaleItem
        fields = ['stone', 'quantity']