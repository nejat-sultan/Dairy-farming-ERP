# Generated by Django 5.0.4 on 2024-08-15 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0020_employee_leave_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='original_hire_date',
            field=models.DateField(null=True),
        ),
    ]
