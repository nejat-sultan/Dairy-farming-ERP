# Generated by Django 5.0.4 on 2024-06-13 08:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0009_farm_farmaddress_farmcontacts'),
    ]

    operations = [
        migrations.AddField(
            model_name='farm',
            name='country',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='farm',
            name='house_number',
            field=models.CharField(max_length=45, null=True),
        ),
        migrations.AddField(
            model_name='farm',
            name='kebele',
            field=models.CharField(max_length=45, null=True),
        ),
        migrations.AddField(
            model_name='farm',
            name='region',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='erp.region'),
        ),
        migrations.AddField(
            model_name='farm',
            name='woreda',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='farm',
            name='zone_subcity',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='farm',
            name='full_name',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='farm',
            name='modified_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='farm',
            name='nick_name',
            field=models.CharField(max_length=45, null=True),
        ),
        migrations.DeleteModel(
            name='FarmAddress',
        ),
    ]