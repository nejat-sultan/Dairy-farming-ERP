# Generated by Django 5.0.4 on 2024-06-10 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0003_rename_person_farm_entity_id_customer_person_farm_entity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockout',
            name='quantity',
            field=models.CharField(max_length=45, null=True),
        ),
    ]
