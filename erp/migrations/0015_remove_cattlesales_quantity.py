# Generated by Django 5.0.4 on 2024-08-06 10:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0014_alter_cattlesales_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cattlesales',
            name='quantity',
        ),
    ]
