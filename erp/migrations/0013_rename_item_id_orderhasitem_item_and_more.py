# Generated by Django 5.0.4 on 2024-05-07 13:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0012_order_orderhasitem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderhasitem',
            old_name='item_id',
            new_name='item',
        ),
        migrations.RenameField(
            model_name='orderhasitem',
            old_name='order_id',
            new_name='order',
        ),
    ]
