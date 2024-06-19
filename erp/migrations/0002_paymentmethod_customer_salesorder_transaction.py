# Generated by Django 5.0.4 on 2024-06-10 08:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('payment_method', models.CharField(max_length=100, null=True)),
                ('modified_date', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'payment_method',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('customer_id', models.AutoField(primary_key=True, serialize=False)),
                ('person_farm_entity_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.person')),
            ],
            options={
                'db_table': 'customer',
            },
        ),
        migrations.CreateModel(
            name='SalesOrder',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('order_date', models.CharField(max_length=45, null=True)),
                ('quantity', models.FloatField()),
                ('unit_price', models.FloatField(null=True)),
                ('total_amount', models.FloatField(null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.customer')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.stock')),
            ],
            options={
                'db_table': 'sales_order',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField(null=True)),
                ('payment_status', models.CharField(max_length=45, null=True)),
                ('modified_date', models.DateTimeField(null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.salesorder')),
                ('payment_method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.paymentmethod')),
            ],
            options={
                'db_table': 'transaction',
            },
        ),
    ]