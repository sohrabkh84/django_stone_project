from django.db import models

class Person(models.Model):
    PERSON_TYPES = [
        ('real', 'حقیقی'),
        ('legal', 'حقوقی'),
    ]

    first_name = models.CharField(max_length=100, verbose_name='نام')
    last_name = models.CharField(max_length=100, verbose_name='نام خانوادگی')

    national_code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='کد ملی / شناسه اقتصادی'
    )

    phone = models.CharField(max_length=15, verbose_name='شماره تماس')
    address = models.TextField(verbose_name='آدرس')

    person_type = models.CharField(
        max_length=10,
        choices=PERSON_TYPES,
        verbose_name='نوع شخص'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'شخص'
        verbose_name_plural = 'اشخاص'



class Employee(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)

    position = models.CharField(max_length=100, verbose_name='سمت')
    salary = models.DecimalField(max_digits=12, decimal_places=2)
    hire_date = models.DateField()

    def __str__(self):
        return str(self.person)



class Customer(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)

    customer_code = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return str(self.person)



class Supplier(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)

    company_name = models.CharField(max_length=200)

    def __str__(self):
        return self.company_name



class Unit(models.Model):
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=20)

    def __str__(self):
        return self.name



class StoneCategory(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title




class StoneType(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(StoneCategory, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class Stone(models.Model):
    name = models.CharField(max_length=100)

    stone_type = models.ForeignKey(StoneType, on_delete=models.CASCADE)

    color = models.CharField(max_length=50)
    size = models.CharField(max_length=50)

    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True)

    purchase_price = models.DecimalField(max_digits=12, decimal_places=2)
    sale_price = models.DecimalField(max_digits=12, decimal_places=2)

    stock = models.PositiveIntegerField(default=0)

    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class Purchase(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)

    purchase_date = models.DateTimeField(auto_now_add=True)

    total_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    def update_total(self):
        self.total_amount = sum(item.total_price for item in self.items.all())
        self.save()

    def __str__(self):
        return f"Purchase #{self.id}"



class PurchaseItem(models.Model):
    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE,
        related_name='items'
    )

    stone = models.ForeignKey(Stone, on_delete=models.PROTECT)

    quantity = models.PositiveIntegerField()

    unit_price = models.DecimalField(max_digits=12, decimal_places=2)

    total_price = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        editable=False
    )

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
        self.purchase.update_total()

    def delete(self, *args, **kwargs):
        purchase = self.purchase
        super().delete(*args, **kwargs)
        purchase.update_total()

    def __str__(self):
        return self.stone.name



class Sale(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)

    sale_date = models.DateTimeField(auto_now_add=True)

    total_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    def update_total(self):
        self.total_amount = sum(item.total_price for item in self.items.all())
        self.save()

    def __str__(self):
        return f"Sale #{self.id}"



class SaleItem(models.Model):
    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        related_name='items'
    )

    stone = models.ForeignKey(Stone, on_delete=models.PROTECT)

    quantity = models.PositiveIntegerField()

    unit_price = models.DecimalField(max_digits=12, decimal_places=2)

    total_price = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        editable=False
    )

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
        self.sale.update_total()

    def delete(self, *args, **kwargs):
        sale = self.sale
        super().delete(*args, **kwargs)
        sale.update_total()

    def __str__(self):
        return self.stone.name