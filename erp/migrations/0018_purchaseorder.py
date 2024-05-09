# Generated by Django 5.0.4 on 2024-05-08 14:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0017_inventory'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.item')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.order')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.supplier')),
            ],
            options={
                'db_table': 'purchase_order',
            },
        ),
    ]
