# Generated by Django 5.0.4 on 2024-05-06 16:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0009_shift'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feedformulation',
            old_name='feed_formulation_descriprion',
            new_name='feed_formulation_description',
        ),
    ]
