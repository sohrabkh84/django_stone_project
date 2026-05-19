from django.urls import path

from .views import *


urlpatterns = [
    path('stones/', stone_list, name='stone_list'),
    path('add-stone/', add_stone, name='add_stone'),
    path('edit-stone/<int:id>/', edit_stone, name='edit_stone'),
    path('delete-stone/<int:id>/', delete_stone, name='delete_stone'),
    path('customer_list/', customer_list, name='customer_list'),
    path('add-customer/', add_customer, name='add_customer'),
    path('edit-customer/<int:id>/', edit_customer, name='edit_customer'),
    path('delete-customer/<int:id>/', delete_customer, name='delete_customer'),
    path('purchase/<int:id>/add-item/', add_purchase_item),
    path('sale/<int:id>/add-item/', add_sale_item),
    path('purchases/', purchase_list, name='purchase_list'),
    path('add-purchase/', add_purchase, name='add_purchase'),
    path('sales/', sale_list, name='sale_list'),
    path('add-sale/', add_sale, name='add_sale'),
]