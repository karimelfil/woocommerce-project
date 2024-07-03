# Generated by Django 5.0.6 on 2024-06-27 05:51

import django.contrib.postgres.fields
import django.db.models.deletion
import django.db.models.expressions
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConcreteActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True, null=True)),
                ('time_created', models.TimeField(auto_now_add=True, null=True)),
            ],
            options={
                'db_table': 'concrete_activity',
            },
        ),
        migrations.CreateModel(
            name='integrate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='default value', max_length=255)),
                ('consumer_key', models.CharField(default='default value', max_length=1000)),
                ('secret_key', models.CharField(default='default value', max_length=1000)),
                ('active', models.BooleanField(default=False)),
                ('description', models.CharField(default='default value', max_length=100)),
            ],
            options={
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='ItemBrand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True, null=True)),
                ('time_created', models.TimeField(auto_now_add=True, null=True)),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name_plural': 'item_brand',
                'db_table': 'item_brand',
            },
        ),
        migrations.CreateModel(
            name='ItemCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=255, unique=True)),
                ('depth', models.PositiveIntegerField()),
                ('numchild', models.PositiveIntegerField(default=0)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True, null=True)),
                ('time_created', models.TimeField(auto_now_add=True, null=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
            ],
            options={
                'verbose_name': 'item_category',
                'db_table': 'item_category',
            },
        ),
        migrations.CreateModel(
            name='ItemFamily',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True, null=True)),
                ('time_created', models.TimeField(auto_now_add=True, null=True)),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name_plural': 'item_family',
                'db_table': 'item_family',
            },
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True, null=True)),
                ('time_created', models.TimeField(auto_now_add=True, null=True)),
                ('name', models.CharField(max_length=255)),
                ('weight', models.FloatField(blank=True, null=True)),
                ('length', models.FloatField(blank=True, null=True)),
                ('height', models.FloatField(blank=True, null=True)),
                ('width', models.FloatField(blank=True, null=True)),
                ('material', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Specs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True, null=True)),
                ('time_created', models.TimeField(auto_now_add=True, null=True)),
                ('description', models.TextField(blank=True, null=True, unique=True)),
            ],
            options={
                'verbose_name_plural': 'item_specification',
                'db_table': 'item_specification',
            },
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True, null=True)),
                ('time_created', models.TimeField(auto_now_add=True, null=True)),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name_plural': 'item_tags',
                'db_table': 'item_tags',
            },
        ),
        migrations.CreateModel(
            name='UnitOfMeasurment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True, null=True)),
                ('time_created', models.TimeField(auto_now_add=True, null=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('code', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('type', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('length', 'length'), ('width', 'width'), ('height', 'height'), ('weight', 'weight')], max_length=10), blank=True, default=None, null=True, size=None)),
            ],
            options={
                'verbose_name_plural': 'unit_of_measurement',
                'db_table': 'unit_of_measurement',
            },
        ),
        migrations.CreateModel(
            name='VariationsDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True, null=True)),
                ('time_created', models.TimeField(auto_now_add=True, null=True)),
                ('value', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'variations_detail',
                'db_table': 'variations_detail',
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='VariationsHeader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True, null=True)),
                ('time_created', models.TimeField(auto_now_add=True, null=True)),
                ('attribute', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name_plural': 'variations_header',
                'db_table': 'variations_header',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True, null=True)),
                ('time_created', models.TimeField(auto_now_add=True, null=True)),
                ('name', models.CharField(max_length=255)),
                ('active', models.BooleanField(default=True)),
                ('description', models.TextField(blank=True, default='', null=True)),
                ('role', models.CharField(blank=True, choices=[('template', 'Template'), ('variant', 'Variant'), ('standalone', 'Standalone')], db_default='standalone', default='standalone', max_length=20, null=True)),
                ('sku_code', models.CharField(blank=True, default='', max_length=255, null=True, unique=True)),
                ('barcode_type', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('barcode', models.CharField(blank=True, default='', max_length=255, null=True, unique=True)),
                ('type', models.CharField(choices=[('product', 'Product'), ('service', 'Service')], db_default='product', default='product', max_length=255)),
                ('usage', models.CharField(blank=True, choices=[('goods', 'Goods'), ('raw_material', 'Raw Material'), ('works', 'Works'), ('service', 'Service')], default=None, max_length=255, null=True)),
                ('is_variant', models.BooleanField(default=False)),
                ('tracking_stock_by_variant', models.BooleanField(default=False)),
                ('returnable_item', models.BooleanField(db_default=False, default=False)),
                ('width', models.FloatField(blank=True, default=None, null=True)),
                ('height', models.FloatField(blank=True, default=None, null=True)),
                ('length', models.FloatField(blank=True, default=None, null=True)),
                ('weight', models.FloatField(blank=True, default=None, null=True)),
                ('available_in_pos', models.BooleanField(db_default=False, default=False)),
                ('shelf_life', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('end_of_life', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('allow_sales', models.BooleanField(db_default=True, default=True)),
                ('max_discount_sales', models.DecimalField(blank=True, decimal_places=3, default=None, max_digits=6, null=True)),
                ('default_selling_price', models.DecimalField(blank=True, db_default=0, decimal_places=35, default=0, max_digits=50, null=True)),
                ('default_selling_price_usd', models.DecimalField(blank=True, db_default=0, decimal_places=25, default=0, max_digits=50, null=True)),
                ('default_cost', models.DecimalField(blank=True, db_default=0, decimal_places=25, default=0, max_digits=50, null=True)),
                ('default_cost_usd', models.DecimalField(blank=True, db_default=0, decimal_places=25, default=0, max_digits=50, null=True)),
                ('lead_time', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('minimum_quantity_order', models.FloatField(blank=True, default=None, null=True)),
                ('minimum_quantity_in_stock', models.FloatField(blank=True, default=None, null=True)),
                ('warranty_period', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('allow_negative_stock', models.BooleanField(db_default=False, default=False)),
                ('auto_reorder', models.BooleanField(db_default=False, default=False)),
                ('price', models.FloatField(default=0.0)),
                ('regular_price', models.FloatField(default=0.0)),
                ('sales_price', models.FloatField(default=0.0)),
                ('alternative_items', models.ManyToManyField(blank=True, to='ecommerce.item')),
                ('variant_of', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='variant_of_item', to='ecommerce.item')),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='ecommerce.itembrand')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='item_category', to='ecommerce.itemcategory')),
                ('family', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='ecommerce.itemfamily')),
                ('specs', models.ManyToManyField(blank=True, to='ecommerce.specs')),
                ('tags', models.ManyToManyField(blank=True, to='ecommerce.tags')),
                ('default_purchase_unit_of_measure', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='default_purchase_unit', to='ecommerce.unitofmeasurment')),
                ('default_sale_unit_of_measure', models.ForeignKey(blank=True, default=None, max_length=255, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='default_sales_unit', to='ecommerce.unitofmeasurment')),
                ('height_unit_of_measure', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='height_unit', to='ecommerce.unitofmeasurment')),
                ('length_unit_of_measure', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='length_unit', to='ecommerce.unitofmeasurment')),
                ('unit_of_measure', models.ManyToManyField(blank=True, to='ecommerce.unitofmeasurment')),
                ('weight_unit_of_measure', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='weight_unit', to='ecommerce.unitofmeasurment')),
                ('width_unit_of_measure', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='width_unit', to='ecommerce.unitofmeasurment')),
                ('selected_variations', models.ManyToManyField(blank=True, to='ecommerce.variationsdetail')),
                ('variations', models.ManyToManyField(blank=True, related_name='item_variations', to='ecommerce.variationsdetail')),
            ],
            options={
                'verbose_name': 'Item',
                'db_table': 'Item',
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Itemswarehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True, null=True)),
                ('time_created', models.TimeField(auto_now_add=True, null=True)),
                ('quantity', models.FloatField(db_default=0, default=0)),
                ('net_movement', models.FloatField(db_default=0, default=0)),
                ('quantity_reserved', models.FloatField(db_default=0, default=0)),
                ('branch', models.IntegerField(blank=True, null=True)),
                ('opening', models.BooleanField(default=False)),
                ('opening_quantity', models.IntegerField(default=0)),
                ('stock_quantity', models.GeneratedField(db_persist=True, expression=django.db.models.expressions.CombinedExpression(models.F('opening_quantity'), '+', models.F('net_movement')), output_field=models.FloatField())),
                ('available_for_sale', models.GeneratedField(db_persist=True, expression=django.db.models.expressions.CombinedExpression(django.db.models.expressions.CombinedExpression(models.F('opening_quantity'), '+', models.F('net_movement')), '-', models.F('quantity_reserved')), output_field=models.FloatField())),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ecommerce.item')),
            ],
            options={
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='ItemPackage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True, null=True)),
                ('time_created', models.TimeField(auto_now_add=True, null=True)),
                ('quantity', models.FloatField(default=1)),
                ('barcode', models.CharField(max_length=255)),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ecommerce.item')),
                ('package', models.ForeignKey(null=True, on_delete=django.db.models.expressions.Case, to='ecommerce.package')),
            ],
            options={
                'default_permissions': (),
            },
        ),
        migrations.AddField(
            model_name='variationsdetail',
            name='variation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variations', to='ecommerce.variationsheader'),
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True, null=True)),
                ('time_created', models.TimeField(auto_now_add=True, null=True)),
                ('name', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('address', models.CharField(max_length=255)),
                ('branch', models.IntegerField(blank=True, null=True)),
                ('initial_Data', models.BooleanField(default=False)),
                ('default', models.BooleanField(default=False)),
                ('show_room', models.BooleanField(db_default=False, default=False)),
                ('item', models.ManyToManyField(blank=True, through='ecommerce.Itemswarehouse', to='ecommerce.item')),
            ],
            options={
                'verbose_name_plural': 'warehouse',
                'db_table': 'warehouse',
                'unique_together': {('branch', 'name')},
            },
        ),
        migrations.AddField(
            model_name='itemswarehouse',
            name='warehouse',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='ecommerce.warehouse'),
        ),
        migrations.AlterUniqueTogether(
            name='itemswarehouse',
            unique_together={('item', 'branch', 'warehouse')},
        ),
    ]
