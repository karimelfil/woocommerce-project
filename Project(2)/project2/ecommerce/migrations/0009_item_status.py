# Generated by Django 5.0.6 on 2024-07-01 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0008_itemcategory_parentt'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='status',
            field=models.CharField(blank=True, choices=[('published', 'Published'), ('drafted', 'Drafted')], default='published', max_length=255, null=True),
        ),
    ]