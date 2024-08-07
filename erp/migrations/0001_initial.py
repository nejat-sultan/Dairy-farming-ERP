# Generated by Django 5.0.4 on 2024-06-20 06:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FarmEntity',
            fields=[
                ('farm_entity_id', models.AutoField(primary_key=True, serialize=False)),
                ('modified_date', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'farm_entity',
            },
        ),
        migrations.CreateModel(
            name='CattleBreed',
            fields=[
                ('cattle_breed_id', models.AutoField(primary_key=True, serialize=False)),
                ('cattle_breed_type', models.CharField(max_length=100, null=True)),
                ('cattle_breed_description', models.CharField(max_length=200, null=True)),
                ('modified_date', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'cattle_breed',
            },
        ),
        migrations.CreateModel(
            name='CattleHealthCheckup',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('findings', models.CharField(max_length=255, null=True)),
            ],
            options={
                'db_table': 'cattle_health_checkup',
            },
        ),
        migrations.CreateModel(
            name='CattleStatus',
            fields=[
                ('cattle_status_id', models.AutoField(primary_key=True, serialize=False)),
                ('cattle_status', models.CharField(max_length=100, null=True)),
                ('modified_date', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'cattle_status',
            },
        ),
        migrations.CreateModel(
            name='ContactType',
            fields=[
                ('contact_id', models.AutoField(primary_key=True, serialize=False)),
                ('contact_type', models.CharField(max_length=255)),
                ('contact_type_desc', models.CharField(max_length=255, null=True)),
                ('modified_date', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'contact_type',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('customer_id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'customer',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('department_id', models.AutoField(primary_key=True, serialize=False)),
                ('department_name', models.CharField(max_length=45, null=True)),
            ],
            options={
                'db_table': 'department',
            },
        ),
        migrations.CreateModel(
            name='Farm',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=300, null=True)),
                ('nick_name', models.CharField(max_length=45, null=True)),
                ('country', models.CharField(max_length=100, null=True)),
                ('zone_subcity', models.CharField(max_length=100, null=True)),
                ('woreda', models.CharField(max_length=100, null=True)),
                ('kebele', models.CharField(max_length=45, null=True)),
                ('house_number', models.CharField(max_length=45, null=True)),
                ('modified_date', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'farm',
            },
        ),
        migrations.CreateModel(
            name='FeedFormulation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, null=True)),
                ('start_age_in_weeks', models.CharField(max_length=45, null=True)),
                ('end_age_in_weeks', models.CharField(max_length=45, null=True)),
                ('modified_date', models.CharField(max_length=45, null=True)),
            ],
            options={
                'db_table': 'feed_formulation',
            },
        ),
        migrations.CreateModel(
            name='GuaranteeType',
            fields=[
                ('guarantee_type_id', models.AutoField(primary_key=True, serialize=False)),
                ('guarantee_type', models.CharField(max_length=100, null=True)),
                ('modified_date', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'guarantee_type',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('item_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, null=True)),
                ('modified_date', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'item',
            },
        ),
        migrations.CreateModel(
            name='ItemMeasurement',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('measurement', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=200, null=True)),
                ('modified_date', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'item_measurement',
            },
        ),
        migrations.CreateModel(
            name='ItemType',
            fields=[
                ('item_type_id', models.AutoField(primary_key=True, serialize=False)),
                ('item_type', models.CharField(max_length=100, null=True)),
                ('modified_date', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'item_type',
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('job_id', models.AutoField(primary_key=True, serialize=False)),
                ('job_title', models.CharField(max_length=45)),
                ('job_min_salary', models.FloatField(null=True)),
                ('job_max_salary', models.FloatField(null=True)),
            ],
            options={
                'db_table': 'job',
            },
        ),
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200, null=True)),
                ('benefit', models.CharField(max_length=200, null=True)),
                ('modified_date', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'medicine',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('requested_date', models.DateField(null=True)),
                ('request_approved', models.CharField(max_length=10, null=True)),
                ('request_approved_date', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'order',
            },
        ),
        migrations.CreateModel(
            name='OtherIncomeExpense',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('transaction_date', models.DateTimeField(null=True)),
                ('amount', models.FloatField()),
                ('transaction_type', models.CharField(max_length=45)),
                ('transaction_status', models.CharField(max_length=45)),
                ('reason', models.CharField(max_length=200, null=True)),
                ('modified_date', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'other_income_expense',
            },
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('payment_method', models.CharField(max_length=100, null=True)),
                ('modified_date', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'payment_method',
            },
        ),
        migrations.CreateModel(
            name='PersonTitle',
            fields=[
                ('person_title_id', models.AutoField(primary_key=True, serialize=False)),
                ('person_title', models.CharField(max_length=45, null=True)),
                ('modified_date', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'person_title',
            },
        ),
        migrations.CreateModel(
            name='PersonType',
            fields=[
                ('person_type_id', models.AutoField(primary_key=True, serialize=False)),
                ('person_type', models.CharField(max_length=100, null=True)),
                ('modified_date', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'person_type',
            },
        ),
        migrations.CreateModel(
            name='PregnancyStatus',
            fields=[
                ('pregnancy_status_id', models.AutoField(primary_key=True, serialize=False)),
                ('pregnancy_status', models.CharField(max_length=100, null=True)),
                ('modified_date', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'pregnancy_status',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('region_id', models.AutoField(primary_key=True, serialize=False)),
                ('region', models.CharField(max_length=100, null=True)),
                ('modified_date', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'region',
            },
        ),
        migrations.CreateModel(
            name='SaleType',
            fields=[
                ('sale_type_id', models.AutoField(primary_key=True, serialize=False)),
                ('sale_type', models.CharField(max_length=100, null=True)),
                ('modified_date', models.DateField(null=True)),
            ],
            options={
                'db_table': 'sale_type',
            },
        ),
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('shift_name', models.CharField(max_length=100, null=True)),
                ('shift_start_time', models.DateTimeField(null=True)),
                ('shift_end_time', models.DateTimeField(null=True)),
                ('modified_date', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'shift',
            },
        ),
        migrations.CreateModel(
            name='SupplierType',
            fields=[
                ('supplier_type_id', models.AutoField(primary_key=True, serialize=False)),
                ('supplier_type', models.CharField(max_length=100, null=True)),
                ('modified_date', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'supplier_type',
            },
        ),
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
        migrations.CreateModel(
            name='Vaccine',
            fields=[
                ('vaccine_id', models.AutoField(primary_key=True, serialize=False)),
                ('vaccine_name', models.CharField(max_length=45, null=True)),
                ('vaccine_benefit', models.CharField(max_length=2555, null=True)),
                ('vaccine_recommended_time', models.CharField(max_length=45, null=True)),
            ],
            options={
                'db_table': 'vaccine',
            },
        ),
        migrations.CreateModel(
            name='Cattle',
            fields=[
                ('farm_entity', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='erp.farmentity')),
                ('cattle_ear_id', models.CharField(max_length=30, null=True)),
                ('cattle_date_of_birth', models.DateTimeField(null=True)),
                ('cattle_name', models.CharField(max_length=50, null=True)),
                ('cattle_gender', models.CharField(max_length=15, null=True)),
                ('estimated_price', models.FloatField(blank=True, null=True)),
                ('acquired_status', models.CharField(max_length=45, null=True)),
                ('acquired_date', models.DateTimeField(null=True)),
                ('cattle_breed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.cattlebreed')),
                ('cattle_status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.cattlestatus')),
                ('father', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='father_cattle', to='erp.cattle')),
                ('mother', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mother_cattle', to='erp.cattle')),
            ],
            options={
                'db_table': 'cattle',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('farm_entity', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='erp.farmentity')),
                ('first_name', models.CharField(max_length=150)),
                ('middle_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150, null=True)),
                ('gender', models.CharField(max_length=10, null=True)),
                ('date_of_birth', models.DateField(null=True)),
                ('marital_status', models.CharField(max_length=20, null=True)),
                ('person_title', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='erp.persontitle')),
                ('person_type', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='erp.persontype')),
            ],
            options={
                'db_table': 'person',
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('farm_entity', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='erp.farmentity')),
                ('supplier_name', models.CharField(max_length=250, null=True)),
                ('account_number', models.CharField(max_length=45, null=True)),
                ('supplier_type_id', models.IntegerField()),
            ],
            options={
                'db_table': 'supplier',
            },
        ),
        migrations.CreateModel(
            name='FarmContacts',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('contact', models.CharField(max_length=100)),
                ('contact_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='erp.contacttype')),
                ('farm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.farm')),
            ],
            options={
                'db_table': 'farm_contacts',
            },
        ),
        migrations.CreateModel(
            name='FarmEntityContact',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('contact', models.CharField(max_length=100)),
                ('contact_type', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='erp.contacttype')),
                ('farm_entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.farmentity')),
            ],
            options={
                'db_table': 'farm_entity_contact',
            },
        ),
        migrations.CreateModel(
            name='HealthCheckupSymptoms',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('symptom', models.CharField(max_length=200, null=True)),
                ('modified_date', models.DateTimeField(null=True)),
                ('cattle_health_checkup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.cattlehealthcheckup')),
            ],
            options={
                'db_table': 'health_checkup_symptoms',
            },
        ),
        migrations.CreateModel(
            name='FeedIngredient',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.CharField(max_length=45, null=True)),
                ('modified_date', models.DateTimeField(null=True)),
                ('feed_formulation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.feedformulation')),
                ('item', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='erp.item')),
                ('item_measurement', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='erp.itemmeasurement')),
            ],
            options={
                'db_table': 'feed_ingredient',
            },
        ),
        migrations.CreateModel(
            name='DirectlyAddedItem',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.CharField(max_length=45, null=True)),
                ('description', models.CharField(max_length=45, null=True)),
                ('unit_price', models.FloatField()),
                ('total_price', models.FloatField(null=True)),
                ('approval_status', models.CharField(max_length=45, null=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.item')),
                ('measurement', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='erp.itemmeasurement')),
                ('item_type', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='erp.itemtype')),
            ],
            options={
                'db_table': 'directly_added_items',
            },
        ),
        migrations.CreateModel(
            name='CattleHealthCheckupHasMedicine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('giving_instruction', models.CharField(max_length=250, null=True)),
                ('modified_date', models.DateTimeField(null=True)),
                ('cattle_health_checkup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.cattlehealthcheckup')),
                ('medicine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.medicine')),
            ],
            options={
                'db_table': 'cattle_health_checkup_has_medicine',
            },
        ),
        migrations.AddField(
            model_name='cattlehealthcheckup',
            name='medicines',
            field=models.ManyToManyField(related_name='health_checkups', through='erp.CattleHealthCheckupHasMedicine', to='erp.medicine'),
        ),
        migrations.CreateModel(
            name='OrderHasItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.CharField(max_length=45, null=True)),
                ('extra_charges', models.FloatField(null=True)),
                ('extracharge_reasons', models.CharField(max_length=150, null=True)),
                ('taxes_in_percent', models.FloatField(null=True)),
                ('discount', models.FloatField(null=True)),
                ('modified_date', models.DateTimeField(max_length=45, null=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.item')),
                ('item_measurement', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='erp.itemmeasurement')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.order')),
                ('type', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='erp.itemtype')),
            ],
            options={
                'db_table': 'order_has_item',
            },
        ),
        migrations.CreateModel(
            name='FarmEntityAddress',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('country', models.CharField(max_length=100, null=True)),
                ('zone_subcity', models.CharField(max_length=100, null=True)),
                ('woreda', models.CharField(max_length=100, null=True)),
                ('kebele', models.CharField(max_length=45, null=True)),
                ('house_number', models.CharField(max_length=45, null=True)),
                ('street_name', models.CharField(max_length=250, null=True)),
                ('farm_entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.farmentity')),
                ('region', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='erp.region')),
            ],
            options={
                'db_table': 'farm_entity_address',
            },
        ),
        migrations.AddField(
            model_name='farm',
            name='region',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='erp.region'),
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('stock_id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.CharField(max_length=45)),
                ('approval_status', models.CharField(max_length=45, null=True)),
                ('modified_date', models.DateTimeField(null=True)),
                ('current_unit_price', models.FloatField(null=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.item')),
                ('item_measurement', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='erp.itemmeasurement')),
                ('type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='erp.itemtype')),
            ],
            options={
                'db_table': 'stock',
            },
        ),
        migrations.CreateModel(
            name='SalesOrder',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('order_date', models.DateTimeField(null=True)),
                ('quantity', models.FloatField()),
                ('unit_price', models.FloatField(null=True)),
                ('payment_status', models.CharField(max_length=45, null=True)),
                ('total_amount', models.FloatField(null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.customer')),
                ('payment_method', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='erp.paymentmethod')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.stock')),
            ],
            options={
                'db_table': 'sales_order',
            },
        ),
        migrations.CreateModel(
            name='MilkProduction',
            fields=[
                ('milk_production_id', models.AutoField(primary_key=True, serialize=False)),
                ('amount_in_liter', models.FloatField(null=True)),
                ('milk_time', models.DateTimeField(null=True)),
                ('fat_content', models.FloatField(null=True)),
                ('protein_content', models.FloatField(null=True)),
                ('somatic_cell_count', models.FloatField(null=True)),
                ('duration_in_min', models.FloatField(null=True)),
                ('cattle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.cattle')),
            ],
            options={
                'db_table': 'milk_production',
            },
        ),
        migrations.CreateModel(
            name='CattlePhoto',
            fields=[
                ('cattle_photo_id', models.AutoField(primary_key=True, serialize=False)),
                ('cattle_photo_url', models.CharField(max_length=200, null=True)),
                ('cattle_photo_description', models.CharField(max_length=200, null=True)),
                ('cattle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.cattle')),
            ],
            options={
                'db_table': 'cattle_photo',
            },
        ),
        migrations.AddField(
            model_name='cattlehealthcheckup',
            name='cattle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.cattle'),
        ),
        migrations.CreateModel(
            name='CattleHasVaccine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cattle_given_time', models.DateTimeField(null=True)),
                ('vaccine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.vaccine')),
                ('cattle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.cattle')),
            ],
            options={
                'db_table': 'cattle_has_vaccine',
            },
        ),
        migrations.CreateModel(
            name='CattleHasFeed',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('feed_time', models.DateTimeField(null=True)),
                ('consumption_status', models.CharField(max_length=45, null=True)),
                ('modified_date', models.DateTimeField(null=True)),
                ('feed_formulation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.feedformulation')),
                ('shift', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.shift')),
                ('cattle_farm_entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.cattle')),
            ],
            options={
                'db_table': 'cattle_has_feed',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('person_farm_entity', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='erp.person')),
                ('salary', models.FloatField(null=True)),
                ('hire_date', models.DateField(null=True)),
                ('national_id', models.CharField(max_length=100, null=True)),
                ('available_leave_hours', models.FloatField(null=True)),
                ('status', models.SmallIntegerField(null=True)),
                ('modified_date', models.DateTimeField(null=True)),
                ('contract_type', models.CharField(max_length=30, null=True)),
                ('contract_period_in_month', models.IntegerField(null=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.department')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.job')),
            ],
            options={
                'db_table': 'employee',
            },
        ),
        migrations.AddField(
            model_name='customer',
            name='person_farm_entity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.person'),
        ),
        migrations.AddField(
            model_name='cattlehealthcheckup',
            name='checked_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='erp.person'),
        ),
        migrations.CreateModel(
            name='OrderHasItemSupplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(null=True)),
                ('quantity', models.CharField(max_length=45, null=True)),
                ('status', models.CharField(max_length=45, null=True)),
                ('inventory_status', models.CharField(max_length=45, null=True)),
                ('modified_date', models.DateTimeField(null=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.item')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supplier_items', to='erp.orderhasitem')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.supplier')),
            ],
            options={
                'db_table': 'order_has_item_supplier',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('employee', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='erp.employee')),
            ],
            options={
                'db_table': 'user_profile',
            },
        ),
        migrations.CreateModel(
            name='TaskAssignment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(max_length=45, null=True)),
                ('due_time', models.DateTimeField(null=True)),
                ('approval_status', models.CharField(max_length=45, null=True)),
                ('rating', models.FloatField(null=True)),
                ('shift', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.shift')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.task')),
                ('assigned_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.employee')),
            ],
            options={
                'db_table': 'task_assignment',
            },
        ),
        migrations.CreateModel(
            name='Stockout',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.CharField(max_length=45, null=True)),
                ('status', models.CharField(max_length=45, null=True)),
                ('modified_date', models.DateTimeField(null=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stockout_items', to='erp.item')),
                ('item_type', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='erp.itemtype')),
                ('measurement', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stockout_items', to='erp.itemmeasurement')),
                ('approved_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approved_stockouts', to='erp.employee')),
                ('requested_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stockout_requests', to='erp.employee')),
            ],
            options={
                'db_table': 'stockout',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='request_approved_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='request_approved_orders', to='erp.employee'),
        ),
        migrations.AddField(
            model_name='order',
            name='requested_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='requested_orders', to='erp.employee'),
        ),
        migrations.CreateModel(
            name='JobHistory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('start_date', models.DateField(null=True)),
                ('end_date', models.DateField(null=True)),
                ('salary', models.FloatField(null=True)),
                ('promotion_or_demotion', models.CharField(max_length=45, null=True)),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='erp.department')),
                ('job', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='erp.job')),
                ('person_farm_entity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='erp.employee')),
            ],
            options={
                'db_table': 'job_history',
            },
        ),
        migrations.CreateModel(
            name='Guarantee',
            fields=[
                ('farm_entity', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='erp.farmentity')),
                ('name', models.CharField(max_length=200)),
                ('salary_evaluation', models.FloatField(null=True)),
                ('guarantee_type', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='erp.guaranteetype')),
                ('person_farm_entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.employee')),
            ],
            options={
                'db_table': 'guarantee',
            },
        ),
        migrations.CreateModel(
            name='EmployeeLeave',
            fields=[
                ('leave_id', models.AutoField(primary_key=True, serialize=False)),
                ('start_date', models.DateTimeField(null=True)),
                ('end_date', models.DateTimeField(null=True)),
                ('reason', models.CharField(max_length=100, null=True)),
                ('approval_status', models.CharField(max_length=45, null=True)),
                ('approved_by_farm_entity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approved_leaves', to='erp.employee')),
                ('person_farm_entity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='leaves', to='erp.employee')),
            ],
            options={
                'db_table': 'employee_leave',
            },
        ),
        migrations.CreateModel(
            name='EmployeeExperience',
            fields=[
                ('experience_id', models.AutoField(primary_key=True, serialize=False)),
                ('company', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('start_date', models.DateField(null=True)),
                ('end_date', models.DateField(null=True)),
                ('salary', models.FloatField(null=True)),
                ('person_farm_entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.employee')),
            ],
            options={
                'db_table': 'employee_experience',
            },
        ),
        migrations.CreateModel(
            name='CattlePregnancy',
            fields=[
                ('cattle_pregnancy_id', models.AutoField(primary_key=True, serialize=False)),
                ('cattle_pregnancy_type', models.CharField(max_length=45, null=True)),
                ('cattle_pregnancy_date', models.DateField()),
                ('is_active', models.CharField(max_length=10, null=True)),
                ('pregnancy_status', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='erp.pregnancystatus')),
                ('cattle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.cattle')),
                ('check_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='erp.person')),
                ('data_encoded_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='erp.employee')),
            ],
            options={
                'db_table': 'cattle_pregnancy',
            },
        ),
        migrations.AddField(
            model_name='cattlehealthcheckup',
            name='data_encoded_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='erp.employee'),
        ),
    ]
