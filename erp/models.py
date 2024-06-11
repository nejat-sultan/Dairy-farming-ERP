from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Dashboard:
    amount:int
    description: str

class Region(models.Model):
    region_id = models.AutoField(primary_key=True)
    region = models.CharField(max_length=100, null=True)
    modified_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'region'

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
    contact_type = models.CharField(max_length=255)
    contact_type_desc = models.CharField(max_length=255, null=True)
    modified_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'contact_type'

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
    # manager = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'department'

class FarmEntity(models.Model):
    farm_entity_id = models.AutoField(primary_key=True)
    modified_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'farm_entity'

class FarmEntityContact(models.Model):
    id = models.AutoField(primary_key=True)
    farm_entity = models.ForeignKey(FarmEntity, on_delete=models.CASCADE)
    contact = models.CharField(max_length=100)
    contact_type = models.ForeignKey(ContactType, on_delete=models.CASCADE)

    class Meta:
        db_table = 'farm_entity_contact'

class FarmEntityAddress(models.Model):
    id = models.AutoField(primary_key=True)
    farm_entity = models.ForeignKey(FarmEntity, on_delete=models.CASCADE)
    country = models.CharField(max_length=100, null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    zone_subcity = models.CharField(max_length=100, null=True)
    woreda = models.CharField(max_length=100, null=True)
    kebele = models.CharField(max_length=45, null=True)
    house_number = models.CharField(max_length=45, null=True)
    street_name = models.CharField(max_length=250, null=True)

    class Meta:
        db_table = 'farm_entity_address'

class Person(models.Model):
    farm_entity = models.OneToOneField(FarmEntity, on_delete=models.CASCADE, primary_key=True)
    person_title = models.ForeignKey(PersonTitle, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, null=True)
    gender = models.CharField(max_length=10, null=True)
    date_of_birth = models.DateField(null=True)
    marital_status = models.CharField(max_length=20, null=True)
    person_type = models.ForeignKey(PersonType, on_delete=models.CASCADE)

    class Meta:
        db_table = 'person'

class Employee(models.Model):
    person_farm_entity = models.OneToOneField(Person, on_delete=models.CASCADE, primary_key=True)
    salary = models.FloatField(null=True)
    hire_date = models.DateField(null=True)
    national_id = models.CharField(max_length=100, null=True)
    available_leave_hours = models.FloatField(null=True)
    status = models.SmallIntegerField(null=True)
    modified_date = models.DateTimeField(null=True)
    contract_type = models.CharField(max_length=30, null=True)
    contract_period_in_month = models.IntegerField(null=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    class Meta:
        db_table = 'employee'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'user_profile'

class EmployeeExperience(models.Model):
    experience_id = models.AutoField(primary_key=True)
    company = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    salary = models.FloatField(null=True)
    person_farm_entity = models.ForeignKey(Employee, on_delete=models.CASCADE)

    class Meta:
        db_table = 'employee_experience'

class GuaranteeType(models.Model):
    guarantee_type_id = models.AutoField(primary_key=True)
    guarantee_type = models.CharField(max_length=100, null=True)
    modified_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'guarantee_type'

class Guarantee(models.Model):
    farm_entity = models.OneToOneField(FarmEntity, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=200)
    salary_evaluation = models.FloatField(null=True)
    guarantee_type = models.ForeignKey(GuaranteeType, on_delete=models.CASCADE)
    person_farm_entity = models.ForeignKey(Employee, on_delete=models.CASCADE)

    class Meta:
        db_table = 'guarantee'

class Shift(models.Model):
    id = models.AutoField(primary_key=True)
    shift_name = models.CharField(max_length=100, null=True)
    shift_start_time = models.DateTimeField(null=True)
    shift_end_time = models.DateTimeField(null=True)
    modified_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'shift'

class Task(models.Model):
    id = models.AutoField(primary_key=True) 
    task_name = models.CharField(max_length=200, null=False)
    description = models.CharField(max_length=200, null=True, blank=True)
    modified_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'task'

class TaskAssignment(models.Model):
    id = models.AutoField(primary_key=True)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(Employee, on_delete=models.CASCADE)
    status = models.CharField(max_length=45, null=True)
    due_time = models.DateTimeField(null=True)

    class Meta:
        db_table = 'task_assignment'

class JobHistory(models.Model):
    id = models.AutoField(primary_key=True)
    person_farm_entity = models.ForeignKey(Employee, null=True, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, null=True, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, null=True, on_delete=models.CASCADE)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    salary = models.FloatField(null=True)
    promotion_or_demotion = models.CharField(max_length=45, null=True)

    class Meta:
        db_table = 'job_history'

class EmployeeLeave(models.Model):
    leave_id = models.AutoField(primary_key=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    reason = models.CharField(max_length=100, null=True)
    approval_status = models.CharField(max_length=45, null=True)
    person_farm_entity = models.ForeignKey(Employee, null=True, on_delete=models.CASCADE, related_name='leaves')
    approved_by_farm_entity = models.ForeignKey(Employee, null=True, on_delete=models.SET_NULL, related_name='approved_leaves')

    class Meta:
        db_table = 'employee_leave'




class CattleStatus(models.Model):
    cattle_status_id = models.AutoField(primary_key=True)
    cattle_status = models.CharField(max_length=100, null=True)
    modified_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'cattle_status'

class CattleBreed(models.Model):
    cattle_breed_id = models.AutoField(primary_key=True)
    cattle_breed_type = models.CharField(max_length=100, null=True)
    cattle_breed_description = models.CharField(max_length=200, null=True)
    modified_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'cattle_breed'

class Cattle(models.Model):
    farm_entity = models.OneToOneField(FarmEntity,on_delete=models.CASCADE,primary_key=True)
    cattle_ear_id = models.CharField(max_length=30, null=True, blank=True)
    cattle_date_of_birth = models.DateTimeField(null=True, blank=True)
    cattle_name = models.CharField(max_length=50, null=True, blank=True)
    cattle_gender = models.CharField(max_length=15, null=True, blank=True)
    estimated_price = models.FloatField(null=True, blank=True)
    cattle_breed = models.ForeignKey(CattleBreed,on_delete=models.CASCADE)
    cattle_status = models.ForeignKey(CattleStatus,on_delete=models.CASCADE) 

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
    vaccine_id = models.AutoField(primary_key=True)
    vaccine_name = models.CharField(max_length=45, null=True)
    vaccine_benefit = models.CharField(max_length=2555, null=True)
    vaccine_recommended_time = models.CharField(max_length=45, null=True)

    class Meta:
        db_table = 'vaccine'

class CattleHasVaccine(models.Model):
    cattle = models.ForeignKey(Cattle, on_delete=models.CASCADE)
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    cattle_given_time = models.DateTimeField(null=True)
    
    class Meta:
        db_table = 'cattle_has_vaccine'
        # unique_together = ['cattle_id', 'vaccine_id']

class PregnancyStatus(models.Model):
    pregnancy_status_id = models.AutoField(primary_key=True)
    pregnancy_status = models.CharField(max_length=100, null=True)
    modified_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'pregnancy_status'

class CattlePregnancy(models.Model):
    cattle_pregnancy_id = models.AutoField(primary_key=True)
    cattle_pregnancy_type = models.CharField(max_length=45, null=True)
    cattle_pregnancy_date = models.DateField()
    is_active = models.CharField(max_length=10, null=True)
    cattle = models.ForeignKey(Cattle, on_delete=models.CASCADE)
    pregnancy_status = models.ForeignKey(PregnancyStatus, on_delete=models.CASCADE)
    check_by = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)
    data_encoded_by = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)

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

class Medicine(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, null=True) 
    benefit = models.CharField(max_length=200, null=True) 
    modified_date = models.DateTimeField(null=True) 

    class Meta:
        db_table = 'medicine' 

class CattleHealthCheckup(models.Model):
    id = models.AutoField(primary_key=True)
    cattle = models.ForeignKey(Cattle, on_delete=models.CASCADE)
    findings = models.CharField(max_length=255, null=True)
    checked_by = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)
    data_encoded_by = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'cattle_health_checkup'

class CattleHealthCheckupHasMedicine(models.Model):
    cattle_health_checkup = models.ForeignKey(CattleHealthCheckup, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    giving_instruction = models.CharField(max_length=250, null=True)
    modified_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'cattle_health_checkup_has_medicine'
        # unique_together = (('cattle_health_checkup', 'medicine'),)

class HealthCheckupSymptoms(models.Model):
    id = models.AutoField(primary_key=True)
    symptom = models.CharField(max_length=200, null=True)
    cattle_health_checkup = models.ForeignKey(CattleHealthCheckup, on_delete=models.CASCADE)
    modified_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'health_checkup_symptoms'



class ItemType(models.Model):
    item_type_id = models.AutoField(primary_key=True)
    item_type = models.CharField(max_length=100, null=True)
    modified_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'item_type'

class Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True)
    modified_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'item'

class SupplierType(models.Model):
    supplier_type_id = models.AutoField(primary_key=True)
    supplier_type = models.CharField(max_length=100, null=True)
    modified_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'supplier_type'

class Supplier(models.Model):
    farm_entity = models.OneToOneField('FarmEntity', primary_key=True, on_delete=models.CASCADE)
    supplier_name = models.CharField(max_length=250, null=True)
    account_number = models.CharField(max_length=45, null=True)
    supplier_type_id = models.IntegerField()

    class Meta:
        db_table = 'supplier'

class ItemMeasurement(models.Model):
    id = models.AutoField(primary_key=True)
    measurement = models.CharField(max_length=100)
    description = models.CharField(max_length=200, null=True, blank=True)
    modified_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'item_measurement'

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    requested_by = models.ForeignKey(Employee, on_delete=models.CASCADE,null=True, related_name='requested_orders')
    requested_date = models.DateField(null=True)
    request_approved = models.CharField(max_length=10, null=True)
    request_approved_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='request_approved_orders')
    request_approved_date = models.DateTimeField(null=True)
    purchase_approved = models.CharField(max_length=10, null=True)
    purchase_approved_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='purchase_approved_orders')
    purchase_approved_date = models.DateTimeField(null=True)
    inventory_approved = models.CharField(max_length=10, null=True)
    inventory_approved_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='inventory_approved_orders')
    inventory_approved_date = models.DateTimeField(null=True)
    status = models.CharField(max_length=45, null=True)

    class Meta:
        db_table = 'order'

class OrderHasItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    # type = models.CharField(max_length=45, null=True)
    type = models.ForeignKey(ItemType, on_delete=models.CASCADE, null=True)
    quantity = models.CharField(max_length=45, null=True)
    item_measurement = models.ForeignKey(ItemMeasurement, null=True, on_delete=models.SET_NULL)
    extra_charges = models.FloatField(null=True)
    extracharge_reasons = models.CharField(max_length=150, null=True)
    taxes_in_percent = models.FloatField(null=True)
    discount = models.FloatField(null=True)
    modified_date = models.DateTimeField(max_length=45, null=True)

    class Meta:
        db_table = 'order_has_item'
        # unique_together = ('order', 'item',)

class OrderHasItemSupplier(models.Model):
    order = models.ForeignKey(OrderHasItem, on_delete=models.CASCADE, related_name='supplier_items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    price = models.FloatField(null=True)
    quantity = models.CharField(max_length=45, null=True)
    status = models.CharField(max_length=45, null=True)
    inventory_status = models.CharField(max_length=45, null=True)
    modified_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'order_has_item_supplier'
        # unique_together = ('order', 'item', 'supplier')

class Stock(models.Model):
    stock_id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=45)
    # type = models.CharField(max_length=45, null=True)
    type = models.ForeignKey(ItemType, on_delete=models.CASCADE, null=True)
    approval_status = models.CharField(max_length=45, null=True)
    modified_date = models.DateTimeField(null=True)
    item_measurement = models.ForeignKey(ItemMeasurement, null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'stock'

class DirectlyAddedItem(models.Model):
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=45, null=True)
    measurement = models.ForeignKey(ItemMeasurement, on_delete=models.SET_NULL, null=True)
    # item_type = models.CharField(max_length=200, null=True)
    item_type = models.ForeignKey(ItemType, on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=45, null=True)
    unit_price = models.FloatField()
    total_price = models.FloatField(null=True)
    approval_status = models.CharField(max_length=45, null=True)

    class Meta:
        db_table = 'directly_added_items'

class Stockout(models.Model):
    id = models.AutoField(primary_key=True)
    requested_by = models.ForeignKey(Employee, on_delete=models.CASCADE,null=True, related_name='stockout_requests')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='stockout_items')
    # item_type = models.CharField(max_length=200, null=True)
    item_type = models.ForeignKey(ItemType, on_delete=models.CASCADE, null=True)
    measurement = models.ForeignKey(ItemMeasurement, on_delete=models.SET_NULL, null=True, related_name='stockout_items')
    approved_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='approved_stockouts')
    # quantity = models.IntegerField()
    quantity = models.CharField(max_length=45, null=True) 
    status = models.CharField(max_length=45, null=True)
    modified_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'stockout'



class FeedFormulation(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True)
    start_age_in_weeks = models.CharField(max_length=45, null=True)
    end_age_in_weeks = models.CharField(max_length=45, null=True)
    modified_date = models.CharField(max_length=45, null=True)

    class Meta:
        db_table = 'feed_formulation'

class FeedIngredient(models.Model):
    id = models.AutoField(primary_key=True)
    feed_formulation = models.ForeignKey(FeedFormulation, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    item_measurement = models.ForeignKey(ItemMeasurement, on_delete=models.CASCADE, null=True)
    quantity = models.CharField(max_length=45, null=True) 
    modified_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'feed_ingredient'

class CattleHasFeed(models.Model):
    id = models.AutoField(primary_key=True)
    cattle_farm_entity = models.ForeignKey(Cattle, on_delete=models.CASCADE)
    feed_formulation = models.ForeignKey(FeedFormulation, on_delete=models.CASCADE)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    feed_time = models.DateTimeField(null=True)
    consumption_status = models.CharField(max_length=45, null=True)
    modified_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'cattle_has_feed'



class SaleType(models.Model):
    sale_type_id = models.AutoField(primary_key=True)
    sale_type = models.CharField(max_length=100, null=True)
    modified_date = models.DateField(null=True)

    class Meta:
        db_table = 'sale_type'

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    person_farm_entity = models.ForeignKey('Person', on_delete=models.CASCADE)

    class Meta:
        db_table = 'customer'

class PaymentMethod(models.Model):
    id = models.AutoField(primary_key=True)
    payment_method = models.CharField(max_length=100, null=True)
    modified_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'payment_method'

class SalesOrder(models.Model):
    id = models.AutoField(primary_key=True)
    order_date = models.CharField(max_length=45, null=True)
    quantity = models.FloatField()
    unit_price = models.FloatField(null=True)
    payment_status = models.CharField(max_length=45, null=True)
    total_amount = models.FloatField(null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'sales_order'








