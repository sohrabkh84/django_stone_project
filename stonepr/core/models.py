from django.db import models

class Person(models.Model):
    PERSON_TYPES = [
        ('real', 'حقیقی'),
        ('legal', 'حقوقی'),
    ]

    first_name = models.CharField(
        max_length=100,
        verbose_name='نام'
    )

    last_name = models.CharField(
        max_length=100,
        verbose_name='نام خانوادگی'
    )

    national_code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='کد ملی / شناسه اقتصادی'
    )

    phone = models.CharField(
        max_length=15,
        verbose_name='شماره تماس'
    )

    address = models.TextField(
        verbose_name='آدرس'
    )

    person_type = models.CharField(
        max_length=10,
        choices=PERSON_TYPES,
        verbose_name='نوع شخص'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ثبت'
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'شخص'
        verbose_name_plural = 'اشخاص'
class Employee(models.Model):
    person = models.OneToOneField(
        Person,
        on_delete=models.CASCADE,
        verbose_name='شخص'
    )

    position = models.CharField(
        max_length=100,
        verbose_name='سمت'
    )

    salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='حقوق'
    )

    hire_date = models.DateField(
        verbose_name='تاریخ استخدام'
    )

    def __str__(self):
        return str(self.person)

    class Meta:
        verbose_name = 'کارمند'
        verbose_name_plural = 'کارمندان'
class Customer(models.Model):
    person = models.OneToOneField(
        Person,
        on_delete=models.CASCADE,
        verbose_name='شخص'
    )

    customer_code = models.CharField(
        max_length=30,
        unique=True,
        verbose_name='کد مشتری'
    )

    def __str__(self):
        return str(self.person)

    class Meta:
        verbose_name = 'مشتری'
        verbose_name_plural = 'مشتریان'
class Supplier(models.Model):
    person = models.OneToOneField(
        Person,
        on_delete=models.CASCADE,
        verbose_name='شخص'
    )

    company_name = models.CharField(
        max_length=200,
        verbose_name='نام شرکت'
    )

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name = 'تامین کننده'
        verbose_name_plural = 'تامین کنندگان'
class Unit(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='نام واحد'
    )

    symbol = models.CharField(
        max_length=20,
        verbose_name='نماد واحد'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'واحد'
        verbose_name_plural = 'واحدها'
class StoneCategory(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='دسته بندی'
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='توضیحات'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته سنگ'
        verbose_name_plural = 'دسته های سنگ'
class StoneType(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='نوع سنگ'
    )

    category = models.ForeignKey(
        StoneCategory,
        on_delete=models.CASCADE,
        verbose_name='دسته بندی'
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='توضیحات'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'نوع سنگ'
        verbose_name_plural = 'انواع سنگ'
class Stone(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='نام سنگ'
    )

    stone_type = models.ForeignKey(
        StoneType,
        on_delete=models.CASCADE,
        verbose_name='نوع سنگ'
    )

    color = models.CharField(
        max_length=50,
        verbose_name='رنگ'
    )

    size = models.CharField(
        max_length=50,
        verbose_name='ابعاد'
    )

    unit = models.ForeignKey(
        Unit,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='واحد'
    )

    purchase_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='قیمت خرید'
    )

    sale_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='قیمت فروش'
    )

    stock = models.PositiveIntegerField(
        default=0,
        verbose_name='موجودی'
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='توضیحات'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ثبت'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'سنگ'
        verbose_name_plural = 'سنگ ها'
class Purchase(models.Model):
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        verbose_name='تامین کننده'
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='ثبت کننده'
    )

    purchase_date = models.DateField(
        verbose_name='تاریخ خرید',
        auto_now_add=True,
    )

    total_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
        verbose_name='مبلغ کل'
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='توضیحات'
    )

    def __str__(self):
        return f"Purchase #{self.id}"

    class Meta:
        verbose_name = 'خرید'
        verbose_name_plural = 'خریدها'
class PurchaseItem(models.Model):
    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='خرید'
    )

    stone = models.ForeignKey(
        Stone,
        on_delete=models.CASCADE,
        verbose_name='سنگ'
    )

    quantity = models.PositiveIntegerField(
        verbose_name='تعداد'
    )

    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='قیمت واحد'
    )

    total_price = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        verbose_name='قیمت کل'
    )

    def __str__(self):
        return str(self.purchase)

    class Meta:
        verbose_name = 'آیتم خرید'
        verbose_name_plural = 'آیتم های خرید'
class Sale(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        verbose_name='مشتری'
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='فروشنده'
    )

    sale_date = models.DateField(
        verbose_name='تاریخ فروش'
    )

    total_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
        verbose_name='مبلغ کل'
    )

    def __str__(self):
        return f"Sale #{self.id}"

    class Meta:
        verbose_name = 'فروش'
        verbose_name_plural = 'فروش ها'
class SaleItem(models.Model):
    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='فروش'
    )

    stone = models.ForeignKey(
        Stone,
        on_delete=models.CASCADE,
        verbose_name='سنگ'
    )

    quantity = models.PositiveIntegerField(
        verbose_name='تعداد'
    )

    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='قیمت واحد'
    )

    total_price = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        verbose_name='قیمت کل'
    )

    def __str__(self):
        return str(self.sale)

    class Meta:
        verbose_name = 'آیتم فروش'
        verbose_name_plural = 'آیتم های فروش'