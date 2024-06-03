# Generated by Django 5.0.4 on 2024-06-03 06:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('task_name', models.CharField(max_length=200)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('modified_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'task',
            },
        ),
        migrations.RenameField(
            model_name='shift',
            old_name='shift_id',
            new_name='id',
        ),
        migrations.AddField(
            model_name='shift',
            name='modified_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='shift',
            name='shift_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.CreateModel(
            name='TaskAssignment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(max_length=45, null=True)),
                ('due_time', models.DateTimeField(null=True)),
                ('assigned_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.employee')),
                ('shift', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.shift')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.task')),
            ],
            options={
                'db_table': 'task_assignment',
            },
        ),
    ]
