# Generated by Django 5.0.4 on 2024-06-25 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0009_remove_cattlepregnancy_check_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='status',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
