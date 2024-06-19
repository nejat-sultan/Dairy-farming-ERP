# Generated by Django 5.0.4 on 2024-06-18 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0011_cattle_acquired_status_cattle_father_cattle_mother'),
    ]

    operations = [
        migrations.AddField(
            model_name='cattle',
            name='acquired_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='cattle',
            name='cattle_date_of_birth',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='cattle',
            name='cattle_ear_id',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='cattle',
            name='cattle_gender',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='cattle',
            name='cattle_name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]