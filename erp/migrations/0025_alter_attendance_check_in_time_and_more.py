# Generated by Django 5.0.4 on 2024-08-25 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0024_attendance_check_out_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='check_in_time',
            field=models.TimeField(auto_now_add=True),
        ),
        migrations.AlterUniqueTogether(
            name='attendance',
            unique_together={('employee', 'date')},
        ),
        migrations.DeleteModel(
            name='QRCode',
        ),
    ]