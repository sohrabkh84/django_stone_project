from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('stones/', stone_list, name='stone_list'),
    path('add-stone/', add_stone, name='add_stone'),
    path('edit-stone/<int:id>/', edit_stone, name='edit_stone'),
    path('delete-stone/<int:id>/', delete_stone, name='delete_stone'),
    path('customer_list/', customer_list, name='customer_list'),
    path('add_customer/', add_customer, name='add_customer'),
    path('edit-customer/<int:id>/', edit_customer, name='edit_customer'),
    path('delete-customer/<int:id>/', delete_customer, name='delete_customer'),
    path('purchases/', purchase_list, name='purchase_list'),
    path('add-purchase/', add_purchase, name='add_purchase'),
    path('purchase/<int:id>/add-item/', add_purchase_item, name='add_purchase_item'),
    path('sales/', sale_list, name='sale_list'),
    path('add-sale/', add_sale, name='add_sale'),
    path('sale/<int:id>/add-item/', add_sale_item, name='add_sale_item'),
    path('suppliers/', supplier_list, name='supplier_list'),
    path('add-supplier/', add_supplier, name='add_supplier'),
    path('edit-supplier/<int:id>/', edit_supplier, name='edit_supplier'),
    path('delete-supplier/<int:id>/', delete_supplier, name='delete_supplier'),
    path('persons/', person_list, name='person_list'),
    path('add-person/', add_person, name='add_person'),
    path('edit-person/<int:id>/', edit_person, name='edit_person'),
    path('delete-person/<int:id>/', delete_person, name='delete_person'),
]