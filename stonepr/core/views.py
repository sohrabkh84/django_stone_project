from django.shortcuts import render , redirect , get_list_or_404 , get_object_or_404
from .models import *
from .form import *
from django.http import *

def stone_list(request):

    stones = Stone.objects.all()

    context = {
        'stones': stones
    }

    return render(request, 'core/stone_list.html', context)
def add_stone(request):
    if request.method== "POST" :
        form = StoneForm(request.POST)
        if  form.is_valid():
            form.save()
            return redirect(stone_list)
    else:

        form = StoneForm()

    context = {
        'form': form
    }

    return render(request, 'core/add_stone.html', context)
def edit_stone(request, id):

    stone = get_object_or_404(Stone, id=id)

    if request.method == 'POST':

        form = StoneForm(request.POST, instance=stone)

        if form.is_valid():

            form.save()

            return redirect('stone_list')

    else:

        form = StoneForm(instance=stone)

    context = {
        'form': form
    }
    return render(request, 'core/edit_stone.html', context)

def delete_stone(request, id):
    stone = get_object_or_404(Stone, id=id)
    stone.delete()
    return redirect('stone_list')



def customer_list(request):
    customer = Customer.objects.all()
    return render(request, 'core/customer_list.html', {
        'customers': customer
    })
def add_customer(request):

    if request.method == 'POST':

        form = CustomerForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('customer_list')

    else:
        form = CustomerForm()

    return render(request, 'core/add_customer.html', {
        'form': form
    })
def edit_customer(request, id):

    customer = get_object_or_404(Customer, id=id)

    if request.method == 'POST':

        form = CustomerForm(request.POST, instance=customer)

        if form.is_valid():
            form.save()
            return redirect('customer_list')

    else:
        form = CustomerForm(instance=customer)

    return render(request, 'core/edit_customer.html', {
        'form': form
    })
def delete_customer(request, id):

    customer = get_object_or_404(Customer, id=id)
    customer.delete()

    return redirect('customer_list')
def purchase_list(request):

    purchases = Purchase.objects.all().order_by('-id')

    return render(request, 'core/purchase_list.html', {
        'purchases': purchases
    })
def add_purchase(request):

    suppliers = Supplier.objects.all()
    employees = Employee.objects.all()
    stones = Stone.objects.all()

    if request.method == "POST":

        supplier = Supplier.objects.get(
            id=request.POST['supplier']
        )

        employee = Employee.objects.get(
            id=request.POST['employee']
        )

        stone = Stone.objects.get(
            id=request.POST['stone']
        )

        quantity = int(request.POST['quantity'])

        # ساخت خرید
        purchase = Purchase.objects.create(
            supplier=supplier,
            employee=employee
        )

        # ساخت آیتم خرید
        PurchaseItem.objects.create(
            purchase=purchase,
            stone=stone,
            quantity=quantity,
            price=stone.purchase_price
        )

        # افزایش موجودی
        stone.stock += quantity
        stone.save()

        return redirect('purchase_list')

    return render(request, 'core/add_purchase.html', {
        'suppliers': suppliers,
        'employees': employees,
        'stones': stones
    })
def sale_list(request):

    sales = Sale.objects.all().order_by('-id')

    return render(request, 'core/sale_list.html', {
        'sales': sales
    })
def add_sale(request):

    if request.method == "POST":

        customer = Customer.objects.get(id=request.POST['customer'])
        employee = Employee.objects.get(id=request.POST['employee'])

        sale = Sale.objects.create(
            customer=customer,
            employee=employee
        )

        return redirect('add_sale_item', sale.id)

    return render(request, 'core/add_sale.html', {
        'customers': Customer.objects.all(),
        'employees': Employee.objects.all()
    })
def add_purchase_item(request, purchase_id):

    purchase = Purchase.objects.get(id=purchase_id)

    if request.method == "POST":

        stone_id = request.POST['stone']
        qty = int(request.POST['quantity'])

        stone = Stone.objects.get(id=stone_id)

        PurchaseItem.objects.create(
            purchase=purchase,
            stone=stone,
            quantity=qty,
            price=stone.purchase_price
        )

        stone.stock += qty
        stone.save()

        return redirect('purchase_detail', purchase.id)
def add_sale_item(request, sale_id):

    sale = Sale.objects.get(id=sale_id)

    if request.method == "POST":

        stone_id = request.POST['stone']
        qty = int(request.POST['quantity'])

        stone = Stone.objects.get(id=stone_id)

        SaleItem.objects.create(
            sale=sale,
            stone=stone,
            quantity=qty,
            price=stone.sale_price
        )

        stone.stock -= qty
        stone.save()

        return redirect('sale_detail', sale.id)
def supplier_list(request):

    suppliers = Supplier.objects.all()

    return render(request, 'core/supplier_list.html', {
        'suppliers': suppliers
    })
def add_supplier(request):

    if request.method == 'POST':

        form = SupplierForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('supplier_list')

    else:

        form = SupplierForm()

    return render(request, 'core/add_supplier.html', {
        'form': form
    })
def edit_supplier(request, id):

    supplier = get_object_or_404(Supplier, id=id)

    if request.method == 'POST':

        form = SupplierForm(request.POST, instance=supplier)

        if form.is_valid():

            form.save()

            return redirect('supplier_list')

    else:

        form = SupplierForm(instance=supplier)

    return render(request, 'core/edit_supplier.html', {
        'form': form
    })
def delete_supplier(request, id):

    supplier = get_object_or_404(Supplier, id=id)

    supplier.delete()

    return redirect('supplier_list')

def person_list(request):

    persons = Person.objects.all()

    return render(request, 'core/person_list.html', {
        'persons': persons
    })
def add_person(request):

    if request.method == 'POST':

        form = PersonForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('person_list')

    else:

        form = PersonForm()

    return render(request, 'core/add_person.html', {
        'form': form
    })

def edit_person(request, id):

    person = get_object_or_404(Person, id=id)

    if request.method == 'POST':

        form = PersonForm(request.POST, instance=person)

        if form.is_valid():

            form.save()

            return redirect('person_list')

    else:

        form = PersonForm(instance=person)

    return render(request, 'core/edit_person.html', {
        'form': form
    })
def delete_person(request, id):

    person = get_object_or_404(Person, id=id)

    person.delete()

    return redirect('person_list')