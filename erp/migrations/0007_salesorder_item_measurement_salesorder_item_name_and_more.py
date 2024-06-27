# Generated by Django 5.0.4 on 2024-06-24 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0006_alter_salesorder_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesorder',
            name='item_measurement',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='salesorder',
            name='item_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='salesorder',
            name='item_type',
            field=models.CharField(max_length=100, null=True),
        ),
    ]