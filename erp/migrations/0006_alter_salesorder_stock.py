# Generated by Django 5.0.4 on 2024-06-24 07:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0005_department_manager_alter_employee_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salesorder',
            name='stock',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='erp.stock'),
        ),
    ]
