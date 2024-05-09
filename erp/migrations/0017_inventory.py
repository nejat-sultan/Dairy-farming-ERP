# Generated by Django 5.0.4 on 2024-05-08 13:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0016_orderhasitemsupplier'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('inventory_id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.CharField(max_length=45, null=True)),
                ('unit_price', models.CharField(max_length=45, null=True)),
                ('measurement', models.CharField(max_length=100, null=True)),
                ('type', models.CharField(max_length=45, null=True)),
                ('description', models.CharField(max_length=200, null=True)),
                ('modified_date', models.DateTimeField(null=True)),
                ('item_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.item')),
            ],
            options={
                'db_table': 'inventory',
            },
        ),
    ]
