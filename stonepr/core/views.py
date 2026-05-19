from django.shortcuts import render , redirect
from .models import Stone
from .form import *


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

    if request.method == "POST":

        supplier_id = request.POST['supplier']
        employee_id = request.POST['employee']

        supplier = Supplier.objects.get(id=supplier_id)
        employee = Employee.objects.get(id=employee_id)

        purchase = Purchase.objects.create(
            supplier=supplier,
            employee=employee
        )

        return redirect('add_purchase_item', purchase.id)

    return render(request, 'core/add_purchase.html', {
        'suppliers': Supplier.objects.all(),
        'employees': Employee.objects.all()
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