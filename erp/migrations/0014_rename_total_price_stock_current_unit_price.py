# Generated by Django 5.0.4 on 2024-06-18 13:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0013_stock_total_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stock',
            old_name='total_price',
            new_name='current_unit_price',
        ),
    ]