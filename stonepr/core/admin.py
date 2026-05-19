from django.contrib import admin
from core.models import *

admin.site.register(Person)
admin.site.register(Employee)
admin.site.register(Customer)
admin.site.register(Supplier)
admin.site.register(Unit)
admin.site.register(StoneCategory)
admin.site.register(StoneType)
admin.site.register(Stone)
admin.site.register(Purchase)
admin.site.register(PurchaseItem)
admin.site.register(SaleItem)
admin.site.register(Sale)