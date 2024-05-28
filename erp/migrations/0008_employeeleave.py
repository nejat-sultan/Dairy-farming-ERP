# Generated by Django 5.0.4 on 2024-05-27 07:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0007_alter_jobhistory_unique_together_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeLeave',
            fields=[
                ('leave_id', models.AutoField(primary_key=True, serialize=False)),
                ('start_date', models.DateTimeField(null=True)),
                ('end_date', models.DateTimeField(null=True)),
                ('reason', models.CharField(max_length=100, null=True)),
                ('approval_status', models.CharField(max_length=45, null=True)),
                ('approved_by_farm_entity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approved_leaves', to='erp.employee')),
                ('person_farm_entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leaves', to='erp.employee')),
            ],
            options={
                'db_table': 'employee_leave',
            },
        ),
    ]