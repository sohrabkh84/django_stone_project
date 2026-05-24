
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib import messages
from .models import * 
from .forms import *


def stone_list(request):
    stones = Stone.objects.all()
    return render(request, 'core/stone_list.html', {'stones': stones})


def add_stone(request):
    if request.method == "POST":
        form = StoneForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('stone_list')
    else:
        form = StoneForm()

    return render(request, 'core/add_stone.html', {'form': form})


def edit_stone(request, id):
    stone = get_object_or_404(Stone, id=id)

    if request.method == 'POST':
        form = StoneForm(request.POST, instance=stone)
        if form.is_valid():
            form.save()
            return redirect('stone_list')
    else:
        form = StoneForm(instance=stone)

    return render(request, 'core/edit_stone.html', {'form': form})


def delete_stone(request, id):
    stone = get_object_or_404(Stone, id=id)
    stone.delete()
    return redirect('stone_list')


def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'core/customer_list.html', {'customers': customers})


def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()

    return render(request, 'core/add_customer.html', {'form': form})


def edit_customer(request, id):
    customer = get_object_or_404(Customer, id=id)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)

    return render(request, 'core/edit_customer.html', {'form': form})


def delete_customer(request, id):
    customer = get_object_or_404(Customer, id=id)
    customer.delete()
    return redirect('customer_list')


def purchase_list(request):
    purchases = Purchase.objects.all().order_by('-id')
    return render(request, 'core/purchase_list.html', {'purchases': purchases})


def add_purchase(request):
    if request.method == "POST":
        supplier_id = request.POST.get('supplier')
        employee_id = request.POST.get('employee')
        stone_id = request.POST.get('stone')
        quantity_str = request.POST.get('quantity')

        if not all([supplier_id, employee_id, stone_id, quantity_str]):
            return render(request, 'core/add_purchase.html', {
                'suppliers': Supplier.objects.all(),
                'employees': Employee.objects.all(),
                'stones': Stone.objects.all(),
                'error': 'All fields are required.'
            })

        try:
            quantity = int(quantity_str)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            return render(request, 'core/add_purchase.html', {
                'suppliers': Supplier.objects.all(),
                'employees': Employee.objects.all(),
                'stones': Stone.objects.all(),
                'error': 'Quantity must be a positive integer.'
            })

        supplier = get_object_or_404(Supplier, id=supplier_id)
        employee = get_object_or_404(Employee, id=employee_id)
        stone = get_object_or_404(Stone, id=stone_id)

        with transaction.atomic():
            purchase = Purchase.objects.create(
                supplier=supplier,
                employee=employee
            )

            PurchaseItem.objects.create(
                purchase=purchase,
                stone=stone,
                quantity=quantity,
                unit_price=stone.purchase_price
            )

            stone.stock += quantity
            stone.save()

        return redirect('purchase_list')

    return render(request, 'core/add_purchase.html', {
        'suppliers': Supplier.objects.all(),
        'employees': Employee.objects.all(),
        'stones': Stone.objects.all()
    })


def add_purchase_item(request, purchase_id):
    purchase = get_object_or_404(Purchase, id=purchase_id)

    if request.method == "POST":
        stone_id = request.POST.get('stone')
        qty_str = request.POST.get('quantity')

        if not all([stone_id, qty_str]):
            return render(request, 'core/add_purchase_item.html', {
                'purchase': purchase,
                'stones': Stone.objects.all(),
                'error': 'All fields are required.'
            })

        try:
            qty = int(qty_str)
            if qty <= 0:
                raise ValueError
        except ValueError:
            return render(request, 'core/add_purchase_item.html', {
                'purchase': purchase,
                'stones': Stone.objects.all(),
                'error': 'Quantity must be a positive integer.'
            })

        stone = get_object_or_404(Stone, id=stone_id)

        with transaction.atomic():
            PurchaseItem.objects.create(
                purchase=purchase,
                stone=stone,
                quantity=qty,
                unit_price=stone.purchase_price
            )

            stone.stock += qty
            stone.save()

        return redirect('purchase_list')

    return render(request, 'core/add_purchase_item.html', {
        'purchase': purchase,
        'stones': Stone.objects.all()
    })


def sale_list(request):
    sales = Sale.objects.all().order_by('-id')
    return render(request, 'core/sale_list.html', {'sales': sales})


def add_sale(request):
    if request.method == "POST":
        form = SaleForm(request.POST)
        formset = SaleItemFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                # ۱. بررسی اولیه موجودی انبار برای تمام اقلام فاکتور قبل از ذخیره‌سازی
                for item_form in formset.forms:
                    if item_form.cleaned_data and not item_form.cleaned_data.get('DELETE'):
                        stone = item_form.cleaned_data.get('stone')
                        quantity = item_form.cleaned_data.get('quantity')
                        
                        if stone and quantity:
                            if stone.stock < quantity:
                                messages.error(request, f"موجودی سنگ «{stone.name}» کافی نیست. موجودی فعلی: {stone.stock}")
                                return render(request, 'core/add_sale.html', {'form': form, 'formset': formset})

                # ۲. ثبت فاکتور اصلی
                sale = form.save()

                # ۳. ثبت اقلام فاکتور و کسر از انبار
                instances = formset.save(commit=False)
                for instance in instances:
                    instance.sale = sale
                    instance.unit_price = instance.stone.sale_price
                    instance.save()
                    
                    # کسر از موجودی انبار
                    stone = instance.stone
                    stone.stock -= instance.quantity
                    stone.save()

                # ۴. به‌روزرسانی مبلغ کل فاکتور
                sale.update_total()

                # ۵. مدیریت ردیف‌های حذف شده در ویرایش یا فرم‌ست
                for deleted_obj in formset.deleted_objects:
                    deleted_obj.stone.stock += deleted_obj.quantity
                    deleted_obj.stone.save()
                    deleted_obj.delete()
                    sale.update_total()

            return redirect('sale_list')
    else:
        form = SaleForm()
        formset = SaleItemFormSet()

    return render(request, 'core/add_sale.html', {
        'form': form,
        'formset': formset
    })

def add_sale_item(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)

    if request.method == "POST":
        stone_id = request.POST.get('stone')
        qty_str = request.POST.get('quantity')

        if not all([stone_id, qty_str]):
            return render(request, 'core/add_sale_item.html', {
                'sale': sale,
                'stones': Stone.objects.all(),
                'error': 'All fields are required.'
            })

        stone = get_object_or_404(Stone, id=stone_id)

        try:
            qty = int(qty_str)
            if qty <= 0:
                raise ValueError
        except ValueError:
            return render(request, 'core/add_sale_item.html', {
                'sale': sale,
                'stones': Stone.objects.all(),
                'error': 'Quantity must be a positive integer.'
            })

        if stone.stock < qty:
            return render(request, 'core/add_sale_item.html', {
                'sale': sale,
                'stones': Stone.objects.all(),
                'error': f'Not enough stock. Available: {stone.stock}'
            })

        with transaction.atomic():
            SaleItem.objects.create(
                sale=sale,
                stone=stone,
                quantity=qty,
                unit_price=stone.sale_price
            )

            stone.stock -= qty
            stone.save()

        return redirect('sale_list')

    return render(request, 'core/add_sale_item.html', {
        'sale': sale,
        'stones': Stone.objects.all()
    })


def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'core/supplier_list.html', {'suppliers': suppliers})


def add_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm()

    return render(request, 'core/add_supplier.html', {'form': form})


def edit_supplier(request, id):
    supplier = get_object_or_404(Supplier, id=id)

    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm(instance=supplier)

    return render(request, 'core/edit_supplier.html', {'form': form})


def delete_supplier(request, id):
    supplier = get_object_or_404(Supplier, id=id)
    supplier.delete()
    return redirect('supplier_list')


def person_list(request):
    persons = Person.objects.all()
    return render(request, 'core/person_list.html', {'persons': persons})


def add_person(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('person_list')
    else:
        form = PersonForm()

    return render(request, 'core/add_person.html', {'form': form})


def edit_person(request, id):
    person = get_object_or_404(Person, id=id)

    if request.method == 'POST':
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect('person_list')
    else:
        form = PersonForm(instance=person)

    return render(request, 'core/edit_person.html', {'form': form})


def delete_person(request, id):
    person = get_object_or_404(Person, id=id)
    person.delete()
    return redirect('person_list')
def home(request):
    return render(request, 'core/home.html')