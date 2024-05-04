from django.db import models

# Create your models here.
class Dashboard:
    amount:int
    description: str

class CattleStatus(models.Model):
    cattle_status_id = models.AutoField(primary_key=True)
    cattle_status = models.CharField(max_length=100, null=True)
    modified_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'cattle_status'

class PersonType(models.Model):
    person_type_id = models.AutoField(primary_key=True)
    person_type = models.CharField(max_length=100, null=True)
    modified_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'person_type'

class PersonTitle(models.Model):
    person_title_id = models.AutoField(primary_key=True)
    person_title = models.CharField(max_length=45, null=True)
    modified_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'person_title'

class ContactType(models.Model):
    contact_id = models.AutoField(primary_key=True)
    contact_type = models.CharField(max_length=255, null=True)
    contact_type_desc = models.CharField(max_length=255, null=True)
    modified_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'contact_type'

class SupplierType(models.Model):
    supplier_type_id = models.AutoField(primary_key=True)
    supplier_type = models.CharField(max_length=100, null=True)
    modified_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'supplier_type'

class SaleType(models.Model):
    sale_type_id = models.AutoField(primary_key=True)
    sale_type = models.CharField(max_length=100, null=True)
    modified_date = models.DateField(null=True)

    class Meta:
        db_table = 'sale_type'

class Region(models.Model):
    region_id = models.AutoField(primary_key=True)
    region = models.CharField(max_length=100, null=True)
    modified_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'region'

class GuaranteeType(models.Model):
    guarantee_type_id = models.AutoField(primary_key=True)
    guarantee_type = models.CharField(max_length=100, null=True)
    modified_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'guarantee_type'




class CattleBreed(models.Model):
    cattle_breed_id = models.AutoField(primary_key=True)
    cattle_breed_name = models.CharField(max_length=100, null=True)
    cattle_breed_description = models.CharField(max_length=200, null=True)
    modified_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'cattle_breed'

class Cattle(models.Model):
    cattle_id = models.CharField(max_length=30, primary_key=True)
    cattle_date_of_birth = models.DateTimeField(null=True)
    cattle_name = models.CharField(max_length=50, null=True)
    cattle_gender = models.CharField(max_length=15, null=True)
    estimated_price = models.FloatField(null=True)
    cattle_breed = models.ForeignKey(CattleBreed, on_delete=models.CASCADE)
    cattle_status = models.ForeignKey(CattleStatus, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'cattle'

class CattlePhoto(models.Model):
    cattle_photo_id = models.AutoField(primary_key=True)
    cattle_photo_url = models.CharField(max_length=200, null=True)
    cattle_photo_description = models.CharField(max_length=200, null=True)
    cattle = models.ForeignKey(Cattle, on_delete=models.CASCADE)

    class Meta:
        db_table = 'cattle_photo'

class Vaccine(models.Model):
    vaccine_id = models.IntegerField(primary_key=True)
    vaccine_name = models.CharField(max_length=45, null=True)
    vaccine_benefit = models.CharField(max_length=2555, null=True)
    vaccine_recommended_time = models.CharField(max_length=45, null=True)

    class Meta:
        db_table = 'vaccine'

class CattleHasVaccine(models.Model):
    cattle = models.ForeignKey(Cattle, on_delete=models.CASCADE)
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    cattle_given_time = models.DateField(null=True)

    class Meta:
        db_table = 'cattle_has_vaccine'
        # unique_together = ['cattle_id', 'vaccine_id']

class CattlePregnancy(models.Model):
    cattle_pregnancy_id = models.AutoField(primary_key=True)
    cattle_pregnancy_type = models.CharField(max_length=45, null=True)
    cattle_pregnancy_date = models.DateField()
    cattle_expected_delivery_date = models.DateField(null=True)
    cattle = models.ForeignKey(Cattle, on_delete=models.CASCADE)

    class Meta:
        db_table = 'cattle_pregnancy'

class MilkProduction(models.Model):
    milk_production_id = models.AutoField(primary_key=True)
    amount_in_liter = models.FloatField(null=True)
    milk_time = models.DateTimeField(null=True)
    fat_content = models.FloatField(null=True)
    protein_content = models.FloatField(null=True)
    somatic_cell_count = models.FloatField(null=True)
    duration_in_min = models.FloatField(null=True)
    cattle = models.ForeignKey(Cattle, on_delete=models.CASCADE)

    class Meta:
        db_table = 'milk_production'

class Job(models.Model):
    job_id = models.AutoField(primary_key=True)
    job_title = models.CharField(max_length=45)
    job_min_salary = models.FloatField(null=True)
    job_max_salary = models.FloatField(null=True)

    class Meta:
        db_table = 'job'

class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=45, null=True)
    # manager_id = models.ForeignKey(Employee, on_delete=models.CASCADE)

    class Meta:
        db_table = 'department'

class Employee(models.Model):
    person_farm_entity_id = models.AutoField(primary_key=True)
    salary = models.FloatField(null=True)
    hire_date = models.DateField(null=True)
    national_id = models.CharField(max_length=100, null=True)
    availableleavehours = models.FloatField(null=True)
    status = models.SmallIntegerField(null=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    modified_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'employee'

class FeedFormulation(models.Model):
    feed_formulation_id = models.AutoField(primary_key=True)
    feed_formulation_descriprion = models.CharField(max_length=255)

    class Meta:
        db_table = 'feed_formulation'

class FeedTimeCategory(models.Model):
    feed_time_category_id = models.AutoField(primary_key=True)
    feed_time_category = models.CharField(max_length=200, null=True)
    start_time = models.CharField(max_length=45, null=True)
    end_time = models.CharField(max_length=45, null=True)

    class Meta:
        db_table = 'feed_time_category'

class FeedTime(models.Model):
    feed_time_id = models.AutoField(primary_key=True)
    feed_time = models.DateTimeField(null=True)
    feed_time_status = models.CharField(max_length=45, null=True)
    cattle = models.ForeignKey(Cattle, on_delete=models.CASCADE)
    formulation = models.ForeignKey(FeedFormulation, on_delete=models.CASCADE)
    feed_time_category = models.ForeignKey(FeedTimeCategory, on_delete=models.CASCADE)
    person_farm_entity = models.ForeignKey(Employee, on_delete=models.CASCADE)

    class Meta:
        db_table = 'feed_time'


