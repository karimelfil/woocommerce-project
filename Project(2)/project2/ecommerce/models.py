from treebeard.mp_tree import MP_Node
from decimal import Decimal
from django.db import models
from django.contrib.postgres.fields import ArrayField
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_DOWN, ROUND_HALF_EVEN, ROUND_UP, ROUND_DOWN, ROUND_CEILING, ROUND_FLOOR
import os

UNIT_OF_MEASURE_OPTIONS = [
    ('length', 'length'),
    ('width', 'width'),
    ('height', 'height'),
    ('weight', 'weight'),
]

def round_value(value):
    return value

def path_and_rename(instance, filename):
    print('fileenamwee', filename)
    upload_to = 'itemimage/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}{}.{}'.format('item-', instance.sku_code, ext)
    else:
        # set filename as random string
        filename = '{}{}.{}'.format('item-', instance.sku_code, ext)
    # return the whole path to the file
    print('on uploaddd', os.path.join(upload_to, filename))
    return os.path.join(upload_to, filename)

class Activity(models.Model):
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_modified = models.DateTimeField(auto_now=True, null=True)
    time_created = models.TimeField(
        auto_now=False,
        auto_now_add=True,
        null=True,
        blank=True)

    class Meta:
        abstract = True

class ConcreteActivity(Activity):
    pass

    class Meta:
        db_table = "concrete_activity"

class ItemCategory(MP_Node, Activity):
    name = models.CharField(max_length=200, unique=True)
    woocommerce_id=models.IntegerField(default=0)
    image = models.ImageField(null=True, blank=True)
    parentt=models.ForeignKey(        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='parent')
    node_order_by = ['path']
    sibling_order_by = ['path']
    class Meta:
        verbose_name = "item_category"
        db_table = "item_category"

    def __str__(self):
        return self.name
    
class ItemFamily(Activity):
    name = models.CharField(max_length=255, unique=True)
    woocommerce_id=models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "item_family"
        db_table = "item_family"

    def __str__(self):
        return self.name

class ItemBrand(Activity):
    name = models.CharField(max_length=255, unique=True)
    woocommerce_id=models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "item_brand"
        db_table = "item_brand"

    def __str__(self):
        return self.name

class Specs(Activity):
    description = models.TextField(null=True, blank=True, unique=True)
    woocommerce_id=models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "item_specification"
        db_table = "item_specification"

class UnitOfMeasurment(Activity):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=50, unique=True, null=True, blank=True)
    woocommerce_id=models.IntegerField(default=0)
    type = ArrayField(
        models.CharField(max_length=10, choices=UNIT_OF_MEASURE_OPTIONS),
        default=None, blank=True, null=True
    )

    class Meta:
        verbose_name_plural = "unit_of_measurement"
        db_table = "unit_of_measurement"

class Tags(Activity):
    name = models.CharField(max_length=255, unique=True)
    woocommerce_id=models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "item_tags"
        db_table = "item_tags"

class Package(Activity):
    name = models.CharField(max_length=255)
    weight = models.FloatField(null=True, blank=True)
    length = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    width = models.FloatField(null=True, blank=True)
    material = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        default_permissions = ()

class VariationsHeader(Activity):
    attribute = models.CharField(max_length=255, unique=True)
    woocommerce_id=models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "variations_header"
        db_table = "variations_header"

class VariationsDetail(Activity):
    variation = models.ForeignKey(
        VariationsHeader,
        on_delete=models.CASCADE,
        related_name='variations')
    value = models.CharField(max_length=255)
    woocommerce_id=models.IntegerField(default=0)

    class Meta:
        default_permissions = ()
        verbose_name = "variations_detail"
        db_table = "variations_detail"

class Item(Activity):
    # General
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    status= models.CharField(max_length=255,choices=[(
        'published', 'Published'), ('drafted', 'Drafted')], default='published', null=True, blank=True)
    description = models.TextField(blank=True, null=True, default='')
    role = models.CharField(max_length=20, choices=[(
        'template', 'Template'), ('variant', 'Variant'), ('standalone', 'Standalone')],
                            default='standalone', db_default='standalone', null=True, blank=True)
    sku_code = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
        default='')
    barcode_type = models.CharField(max_length=255, null=True, blank=True, default='')
    barcode = models.CharField(
        max_length=255, null=True, unique=True, blank=True, default='')
    type = models.CharField(max_length=255, choices=[('product', 'Product'), (
        'service', 'Service')], default='product', db_default='product')
    # usage have Raw Material, Goods, Works
    usage = models.CharField(max_length=255, choices=[('goods', 'Goods'), (
        'raw_material', 'Raw Material'), ('works', 'Works'), ('service', 'Service')], null=True, blank=True, default=None)

    variant_of = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='variant_of_item'
    )
    unit_of_measure = models.ManyToManyField(UnitOfMeasurment, blank=True)
    tags = models.ManyToManyField(Tags, blank=True)
    family = models.ForeignKey(
        ItemFamily,
        null=True,
        blank=True,
        on_delete=models.PROTECT)
    brand = models.ForeignKey(
        ItemBrand,
        null=True,
        blank=True,
        on_delete=models.PROTECT)
    category = models.ForeignKey(
        ItemCategory,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='item_category')
    specs = models.ManyToManyField(Specs, blank=True)

    is_variant = models.BooleanField(default=False)
    tracking_stock_by_variant = models.BooleanField(default=False)
    variations = models.ManyToManyField(
        VariationsDetail, related_name='item_variations', blank=True)
    selected_variations = models.ManyToManyField(
        VariationsDetail, blank=True)
    alternative_items = models.ManyToManyField(
        to='self', blank=True, symmetrical=False)
    returnable_item = models.BooleanField(default=False, db_default=False)
    # Logistics
    width = models.FloatField(null=True, blank=True, default=None)
    width_unit_of_measure = models.ForeignKey(
        UnitOfMeasurment,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='width_unit',
        default=None)
    height = models.FloatField(null=True, blank=True, default=None)
    height_unit_of_measure = models.ForeignKey(
        UnitOfMeasurment,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='height_unit',
        default=None)
    length = models.FloatField(null=True, blank=True, default=None)
    length_unit_of_measure = models.ForeignKey(
        UnitOfMeasurment,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='length_unit',
        default=None)
    weight = models.FloatField(null=True, blank=True, default=None)
    weight_unit_of_measure = models.ForeignKey(
        UnitOfMeasurment,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='weight_unit',
        default=None)
    # pos
    available_in_pos = models.BooleanField(default=False, db_default=False)
    shelf_life = models.CharField(max_length=255, null=True, blank=True, default='')
    end_of_life = models.CharField(max_length=255, null=True, blank=True, default='')
    # sale
    allow_sales = models.BooleanField(default=True, db_default=True)
    max_discount_sales = models.DecimalField(
        max_digits=6, decimal_places=3, null=True, blank=True, default=None)
    default_sale_unit_of_measure = models.ForeignKey(
        UnitOfMeasurment,
        max_length=255,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='default_sales_unit',
        default=None)
    default_selling_price = models.DecimalField(max_digits=50, decimal_places=35,
                                                default=0, db_default=0, null=True, blank=True)  # in company currency
    default_selling_price_usd = models.DecimalField(max_digits=50, decimal_places=25,
                                                    default=0, db_default=0, null=True, blank=True)  # in usd currency
    # purchase
    default_cost = models.DecimalField(max_digits=50, decimal_places=25,
                                       default=0, db_default=0, null=True, blank=True)  # in company currency
    default_cost_usd = models.DecimalField(max_digits=50, decimal_places=25,
                                           default=0, db_default=0, null=True, blank=True)  # in usd currency
    lead_time = models.CharField(max_length=255, null=True, blank=True, default='')
    minimum_quantity_order = models.FloatField(null=True, blank=True, default=None)
    default_purchase_unit_of_measure = models.ForeignKey(
        UnitOfMeasurment,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='default_purchase_unit',
        default=None)
    # inventory
    minimum_quantity_in_stock = models.FloatField(null=True, blank=True, default=None)
    warranty_period = models.CharField(max_length=255, null=True, blank=True, default='')
    allow_negative_stock = models.BooleanField(default=False, db_default=False)
    auto_reorder = models.BooleanField(default=False, db_default=False)
    # Accounting
    price = models.FloatField(default=0.0)
    regular_price = models.FloatField(default=0.0)
    sales_price = models.FloatField(default=0.0)
    #woocommerce_id 
    woocommerce_id = models.IntegerField(null=True, blank=True, default=None)
    def save(self, *args, **kwargs):
        fields_to_round = ['default_selling_price',
                           'default_selling_price_usd', 'default_cost', 'default_cost_usd']
        for field_name in fields_to_round:
            field_value = getattr(self, field_name)
            if field_value is not None:
                field_value = Decimal(field_value)
                rounded_value = round_value(field_value)
                setattr(self, field_name, rounded_value)

        if self.tracking_stock_by_variant:
            self.role = 'template'
        elif self.variant_of is not None:
            self.role = 'variant'
        elif self.variant_of is None and not self.tracking_stock_by_variant:
            self.role = 'standalone'

        super(Item, self).save(*args, **kwargs)

    class Meta:
        default_permissions = ()
        verbose_name = "Item"
        db_table = "Item"
        
class ItemPackage(Activity):
    item = models.ForeignKey(Item, null=True, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, null=True, on_delete=models.Case)
    quantity = models.FloatField(default=1)
    barcode = models.CharField(max_length=255)

    class Meta:
        default_permissions = ()
    #     verbose_name = "item_package"
    #     db_table  = "item_package"

class integrate(models.Model):
    type=models.CharField(max_length=255,default="default value",unique=True)
    consumer_key=models.CharField(max_length=1000,default="default value")
    secret_key=models.CharField(max_length=1000,default="default value")
    active = models.BooleanField(default=False)
    class Meta:
        default_permissions = ()

class Warehouse(Activity):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255)
    branch = models.IntegerField(blank=True, null=True)
    item = models.ManyToManyField(Item, through='Itemswarehouse', blank=True)
    initial_Data = models.BooleanField(default=False)
    default = models.BooleanField(default=False)
    show_room = models.BooleanField(default=False, db_default=False)
    integrate = models.ForeignKey('integrate', on_delete=models.CASCADE,default="default value")

    class Meta:
        unique_together = ("branch", "name")
        verbose_name_plural = "warehouse"
        db_table = "warehouse"

    def __str__(self):
        return self.name + " in " + str(self.branch)

class Itemswarehouse(Activity):
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.PROTECT,
        null=True,
        blank=True)
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    quantity = models.FloatField(db_default=0, default=0)
    net_movement = models.FloatField(db_default=0, default=0)
    quantity_reserved = models.FloatField(db_default=0, default=0)
    branch = models.IntegerField(null=True, blank=True)
    opening = models.BooleanField(default=False)
    opening_quantity = models.IntegerField(default=0)
    stock_quantity = models.GeneratedField(
        expression=models.F("opening_quantity") + models.F("net_movement"),
        output_field=models.FloatField(),
        db_persist=True,
    )
    available_for_sale = models.GeneratedField(
        expression=models.F("opening_quantity") + models.F("net_movement") -
                   models.F("quantity_reserved"),
        output_field=models.FloatField(),
        db_persist=True,
    )

    def __str__(self):
        if self.warehouse:
            return str(self.quantity) + " " + self.item.name + " in " + \
                self.warehouse.name + " in branch" + str(self.branch)
        else:
            return str(self.quantity) + " " + self.item.name + \
                " in branch" + str(self.branch)

    class Meta:
        unique_together = ("item", "branch", "warehouse")
        default_permissions = ()



#############################################################################################


### customers models :

class BillingAddress(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    company = models.CharField(max_length=255, null=True, blank=True)
    address_1 = models.CharField(max_length=255)
    address_2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    postcode = models.CharField(max_length=20)
    country = models.CharField(max_length=250)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    class Meta:
        default_permissions = ()
        verbose_name = "Billing"
        db_table = "Billing"

    def __str__(self):
        return f"{self.first_name} {self.last_name}, {self.address_1}, {self.city}"


class ShippingAddress(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    company = models.CharField(max_length=255, null=True, blank=True)
    address_1 = models.CharField(max_length=255)
    address_2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    postcode = models.CharField(max_length=20)
    country = models.CharField(max_length=250)
    class Meta:
        default_permissions = ()
        verbose_name = "Shipping"
        db_table = "Shipping"
    def __str__(self):
        return f"{self.first_name} {self.last_name}, {self.address_1}, {self.city}"

class Customer(Activity):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    is_paying_customer = models.BooleanField(default=False)
    avatar_url = models.URLField(null=True, blank=True)
    customerbiling_id=models.ForeignKey(BillingAddress,on_delete=models.CASCADE,related_name='Customer')
    customershipping_id=models.ForeignKey(ShippingAddress,on_delete=models.CASCADE,related_name='Customer')
    woocommerce_id=models.IntegerField(null=True)   
    class Meta:
        default_permissions = ()
        verbose_name = "Customer"
        db_table = "Customer"


    def __str__(self):
        return self.email
    




class Order(Activity):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('on-hold', 'On-Hold'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
        ('failed', 'Failed'),
        ('trash', 'Trash'),
    ]
    CURRENCY_CHOICES = [(currency, currency) for currency in [
        'AED', 'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'ARS', 'AUD', 'AWG', 'AZN', 'BAM', 'BBD', 'BDT', 'BGN', 'BHD', 'BIF', 'BMD', 'BND', 'BOB', 'BRL', 'BSD', 'BTC', 'BTN', 'BWP', 'BYR', 'BZD', 'CAD', 'CDF', 'CHF', 'CLP', 'CNY', 'COP', 'CRC', 'CUC', 'CUP', 'CVE', 'CZK', 'DJF', 'DKK', 'DOP', 'DZD', 'EGP', 'ERN', 'ETB', 'EUR', 'FJD', 'FKP', 'GBP', 'GEL', 'GGP', 'GHS', 'GIP', 'GMD', 'GNF', 'GTQ', 'GYD', 'HKD', 'HNL', 'HRK', 'HTG', 'HUF', 'IDR', 'ILS', 'IMP', 'INR', 'IQD', 'IRR', 'IRT', 'ISK', 'JEP', 'JMD', 'JOD', 'JPY', 'KES', 'KGS', 'KHR', 'KMF', 'KPW', 'KRW', 'KWD', 'KYD', 'KZT', 'LAK', 'LBP', 'LKR', 'LRD', 'LSL', 'LYD', 'MAD', 'MDL', 'MGA', 'MKD', 'MMK', 'MNT', 'MOP', 'MRO', 'MUR', 'MVR', 'MWK', 'MXN', 'MYR', 'MZN', 'NAD', 'NGN', 'NIO', 'NOK', 'NPR', 'NZD', 'OMR', 'PAB', 'PEN', 'PGK', 'PHP', 'PKR', 'PLN', 'PRB', 'PYG', 'QAR', 'RON', 'RSD', 'RUB', 'RWF', 'SAR', 'SBD', 'SCR', 'SDG', 'SEK', 'SGD', 'SHP', 'SLL', 'SOS', 'SRD', 'SSP', 'STD', 'SYP', 'SZL', 'THB', 'TJS', 'TMT', 'TND', 'TOP', 'TRY', 'TTD', 'TWD', 'TZS', 'UAH', 'UGX', 'USD', 'UYU', 'UZS', 'VEF', 'VND', 'VUV', 'WST', 'XAF', 'XCD', 'XOF', 'XPF', 'YER', 'ZAR', 'ZMW'
    ]]
    parent_id = models.IntegerField(null=True, blank=True)
    number = models.CharField(max_length=255, unique=True)
    order_key = models.CharField(max_length=255)
    created_via = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    currency = models.CharField(max_length=50, choices=CURRENCY_CHOICES, default='USD')
    discount_total = models.DecimalField(max_digits=10, decimal_places=2)
    discount_tax = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_total = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_tax = models.DecimalField(max_digits=10, decimal_places=2)
    cart_tax = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    total_tax = models.DecimalField(max_digits=10, decimal_places=2)
    prices_include_tax = models.BooleanField(default=False)
    customer_id = models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='ORDER')
    payment_method = models.CharField(max_length=255)
    date_paid = models.DateTimeField(null=True, blank=True)
    date_completed = models.DateTimeField(null=True, blank=True)
    cart_hash = models.CharField(max_length=255)
    set_paid = models.BooleanField(default=True)
    customerbiling_id=models.ForeignKey(BillingAddress,on_delete=models.CASCADE,related_name='ORDER')
    customershipping_id=models.ForeignKey(ShippingAddress,on_delete=models.CASCADE,related_name='ORDER')
    woocommerce_id=models.IntegerField(null=True)
    class Meta:
        default_permissions = ()
        verbose_name = "Order"
        db_table = "Order"

    def __str__(self):
        return self.number









