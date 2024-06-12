from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index),

    path('register', views.register, name='register'),
    path('login', views.login_page, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('user', views.user, name='user'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('user_delete/<str:id>', views.user_delete),
    path('group', views.group, name='group'),
    path('create_group', views.create_group, name='create_group'),
    path('edit_group/<int:id>/', views.edit_group, name='edit_group'),
    path('group_delete/<str:id>', views.group_delete),
    path('assign_users_to_group/<str:user_id>/', views.assign_users_to_group, name='assign_users_to_group'),

    path('cattle', views.cattle),
    path('cattle_add', views.cattle_add),
    path('cattle_view/<str:farm_entity_id>', views.cattle_view, name='cattle_view'),
    path('cattle_edit/<str:farm_entity_id>', views.cattle_edit, name='cattle_edit'),
    path('cattle_delete/<str:farm_entity_id>', views.cattle_delete),

    path('cattle_status', views.cattle_status),
    path('cattle_status_add', views.cattle_status_add),
    path('cattle_status_edit/<str:cattle_status_id>', views.cattle_status_edit, name='cattle_status_edit'),
    path('cattle_status_delete/<str:cattle_status_id>', views.cattle_status_delete),

    path('cattle_breed', views.cattle_breed),
    path('cattle_breed_add', views.cattle_breed_add),
    path('cattle_breed_edit/<str:cattle_breed_id>', views.cattle_breed_edit, name='cattle_breed_edit'),
    path('cattle_breed_delete/<str:cattle_breed_id>', views.cattle_breed_delete),

    path('pregnancy_status', views.pregnancy_status),
    path('pregnancy_status_add', views.pregnancy_status_add),
    path('pregnancy_status_edit/<str:pregnancy_status_id>', views.pregnancy_status_edit, name='pregnancy_status_edit'),
    path('pregnancy_status_delete/<str:pregnancy_status_id>', views.pregnancy_status_delete),

    path('cattle_pregnancy', views.cattle_pregnancy),
    path('cattle_pregnancy_add', views.cattle_pregnancy_add),
    path('cattle_pregnancy_edit/<str:cattle_pregnancy_id>', views.cattle_pregnancy_edit, name='cattle_pregnancy_edit'),
    path('cattle_pregnancy_delete/<str:cattle_pregnancy_id>', views.cattle_pregnancy_delete),

    path('vaccine', views.vaccine),
    path('vaccine_add', views.vaccine_add),
    path('vaccine_edit/<str:vaccine_id>', views.vaccine_edit, name='vaccine_edit'),
    path('vaccine_delete/<str:vaccine_id>', views.vaccine_delete),

    path('cattle_has_vaccine', views.cattle_has_vaccine),
    path('cattle_has_vaccine_add', views.cattle_has_vaccine_add),
    path('cattle_has_vaccine_edit/<str:id>', views.cattle_has_vaccine_edit, name='cattle_has_vaccine_edit'),
    path('cattle_has_vaccine_delete/<str:id>', views.cattle_has_vaccine_delete),

    path('medicine', views.medicine),
    path('medicine_add', views.medicine_add),
    path('medicine_edit/<str:id>', views.medicine_edit, name='medicine_edit'),
    path('medicine_delete/<str:id>', views.medicine_delete),

    path('cattle_health_checkup', views.cattle_health_checkup),
    path('cattle_health_checkup_view/<str:id>', views.cattle_health_checkup_view, name='cattle_health_checkup_view'),
    path('cattle_health_checkup_add', views.cattle_health_checkup_add),
    path('cattle_health_checkup_edit/<str:id>', views.cattle_health_checkup_edit, name='cattle_health_checkup_edit'),
    path('cattle_health_checkup_delete/<str:id>', views.cattle_health_checkup_delete), 

    path('checkup_medicine_add/<int:id>/', views.checkup_medicine_add, name='checkup_medicine_add'),
    path('checkup_medicine_edit/<str:id>', views.checkup_medicine_edit, name='checkup_medicine_edit'),
    path('checkup_medicine_delete/<str:id>', views.checkup_medicine_delete), 

    path('checkup_symptom_add/<int:id>/', views.checkup_symptom_add, name='checkup_symptom_add'),
    path('checkup_symptom_edit/<str:id>', views.checkup_symptom_edit, name='checkup_symptom_edit'),
    path('checkup_symptom_delete/<str:id>', views.checkup_symptom_delete), 

    path('milk_production', views.milk_production),
    path('milk_production_add', views.milk_production_add),
    path('milk_production_edit/<str:milk_production_id>', views.milk_production_edit, name='milk_production_edit'),
    path('milk_production_delete/<str:milk_production_id>', views.milk_production_delete),

    path('add_photo', views.add_photo),

    path('person_type', views.person_type),
    path('person_type_add', views.person_type_add),
    path('person_type_edit/<str:person_type_id>', views.person_type_edit, name='person_type_edit'),
    path('person_type_delete/<str:person_type_id>', views.person_type_delete),

    path('person_title', views.person_title),
    path('person_title_add', views.person_title_add),
    path('person_title_edit/<str:person_title_id>', views.person_title_edit, name='person_title_edit'),
    path('person_title_delete/<str:person_title_id>', views.person_title_delete),

    path('contact_type', views.contact_type),
    path('contact_type_add', views.contact_type_add),
    path('contact_type_edit/<str:contact_id>', views.contact_type_edit, name='contact_type_edit'),
    path('contact_type_delete/<str:contact_id>', views.contact_type_delete),

    path('supplier_type', views.supplier_type),
    path('supplier_type_add', views.supplier_type_add),
    path('supplier_type_edit/<str:supplier_type_id>', views.supplier_type_edit, name='supplier_type_edit'),
    path('supplier_type_delete/<str:supplier_type_id>', views.supplier_type_delete),

    path('sale_type', views.sale_type),
    path('sale_type_add', views.sale_type_add),
    path('sale_type_edit/<str:sale_type_id>', views.sale_type_edit, name='sale_type_edit'),
    path('sale_type_delete/<str:sale_type_id>', views.sale_type_delete),

    path('customer', views.customer),
    path('customer_add', views.customer_add),
    path('customer_edit/<str:customer_id>', views.customer_edit, name='customer_edit'),
    path('customer_delete/<str:customer_id>', views.customer_delete),
    path('add_customer_contact', views.add_customer_contact),
    path('add_customer_address', views.add_customer_address),

    path('payment_method', views.payment_method),
    path('payment_method_add', views.payment_method_add),
    path('payment_method_edit/<str:id>', views.payment_method_edit, name='payment_method_edit'),
    path('payment_method_delete/<str:id>', views.payment_method_delete),

    path('sales_order', views.sales_order),
    path('sales_order_add', views.sales_order_add),
    path('sales_order_edit/<str:id>', views.sales_order_edit, name='sales_order_edit'),
    path('sales_order_delete/<str:id>', views.sales_order_delete),
    path('get_item_types/<int:item_id>/', views.get_item_types, name='get_item_types'),
    path('get_stock_quantity/<int:item_id>/<int:type_id>/', views.get_stock_quantity, name='get_stock_quantity'),

    path('region', views.region),
    path('region_add', views.region_add),
    path('region_edit/<str:region_id>', views.region_edit, name='region_edit'),
    path('region_delete/<str:region_id>', views.region_delete),
    
    path('guarantee_type', views.guarantee_type),
    path('guarantee_type_add', views.guarantee_type_add),
    path('guarantee_type_edit/<str:guarantee_type_id>', views.guarantee_type_edit, name='guarantee_type_edit'),
    path('guarantee_type_delete/<str:guarantee_type_id>', views.guarantee_type_delete),

    path('shift', views.shift),
    path('shift_add', views.shift_add),
    path('shift_edit/<str:id>', views.shift_edit, name='shift_edit'),
    path('shift_delete/<str:id>', views.shift_delete),

    path('task', views.task),
    path('task_add', views.task_add),
    path('task_edit/<str:id>', views.task_edit, name='task_edit'),
    path('task_delete/<str:id>', views.task_delete),

    path('assign_task', views.assign_task),
    path('assign_task_add', views.assign_task_add),
    path('assign_task_edit/<str:id>', views.assign_task_edit, name='assign_task_edit'),
    path('assign_task_delete/<str:id>', views.assign_task_delete),
    path('update_status', views.update_status),
    path('add_rating', views.add_rating),
    path('approve_task/<int:id>/', views.approve_task, name='approve_task'),
    path('reject_task/<int:id>/', views.reject_task, name='reject_task'),

    path('leave', views.leave),
    path('leave_add', views.leave_add),
    path('leave_view/<str:leave_id>', views.leave_view, name='leave_view'),
    path('leave_edit/<str:leave_id>', views.leave_edit, name='leave_edit'),
    path('leave_delete/<str:leave_id>', views.leave_delete),
    path('approve_leave/<int:leave_id>/', views.approve_leave, name='approve_leave'),
    path('reject_leave/<int:leave_id>/', views.reject_leave, name='reject_leave'),

    path('job', views.job),
    path('job_add', views.job_add),
    path('job_edit/<str:job_id>', views.job_edit, name='job_edit'),
    path('job_delete/<str:job_id>', views.job_delete),

    path('feed_formulation', views.feed_formulation),
    path('feed_formulation_view/<str:id>', views.feed_formulation_view, name='feed_formulation_view'),
    path('feed_formulation_add', views.feed_formulation_add),
    path('feed_formulation_edit/<str:id>', views.feed_formulation_edit, name='feed_formulation_edit'),
    path('feed_formulation_delete/<str:id>', views.feed_formulation_delete),

    path('ingredient_add/<int:id>/', views.ingredient_add, name='ingredient_add'),
    path('ingredient_edit/<str:id>', views.ingredient_edit, name='ingredient_edit'),
    path('ingredient_delete/<str:id>', views.ingredient_delete),

    path('cattle_has_feed', views.cattle_has_feed),
    path('cattle_has_feed_add', views.cattle_has_feed_add),
    path('cattle_has_feed_edit/<str:id>', views.cattle_has_feed_edit, name='cattle_has_feed_edit'),
    path('cattle_has_feed_delete/<str:id>', views.cattle_has_feed_delete),

    path('item_type', views.item_type),
    path('item_type_add', views.item_type_add),
    path('item_type_edit/<str:item_type_id>', views.item_type_edit, name='item_type_edit'),
    path('item_type_delete/<str:item_type_id>', views.item_type_delete),

    path('item', views.item),
    path('item_add', views.item_add),
    path('item_edit/<str:item_id>', views.item_edit, name='item_edit'),
    path('item_delete/<str:item_id>', views.item_delete),

    path('supplier', views.supplier),
    path('supplier_add', views.supplier_add),
    path('supplier_edit/<str:farm_entity_id>', views.supplier_edit, name='supplier_edit'),
    path('supplier_delete/<str:farm_entity_id>', views.supplier_delete),
    path('add_supplier_contact', views.add_supplier_contact),
    path('add_supplier_address', views.add_supplier_address),

    path('request_order', views.request_order),
    path('request_order_view/<str:order_id>', views.request_order_view, name='request_order_view'),
    path('request_order_add', views.request_order_add),
    path('request_order_edit/<str:order_id>', views.request_order_edit, name='request_order_edit'),
    path('request_order_delete/<str:order_id>', views.request_order_delete),
    path('approve_request/<int:order_id>/', views.approve_request, name='approve_request'),
    path('reject_request/<int:order_id>/', views.reject_request, name='reject_request'),

    path('rfq', views.rfq),
    path('rfq_add/<int:order_id>/', views.rfq_add, name='rfq_add'),
    path('rfq_edit/<str:id>', views.rfq_edit, name='rfq_edit'),
    path('rfq_delete/<str:id>', views.rfq_delete),
    path('approve_rfq/<int:id>/', views.approve_rfq, name='approve_rfq'),
    path('reject_rfq/<int:id>/', views.reject_rfq, name='reject_rfq'),

    path('purchase_order', views.purchase_order),
    path('generate_purchase_order/<str:order_id>', views.generate_purchase_order, name='generate_purchase_order'),

    path('approve_inventory/<int:id>/', views.approve_inventory, name='approve_inventory'),
    path('reject_inventory/<int:id>/', views.reject_inventory, name='reject_inventory'),

    path('stock_in', views.stock_in),
    path('stockin_add', views.stockin_add),
    path('stockin_edit/<int:id>', views.stockin_edit, name='stockin_edit'),
    path('stockin_delete/<int:id>', views.stockin_delete),
    path('approve_stockin/<int:id>/', views.approve_stockin, name='approve_stockin'),
    path('reject_stockin/<int:id>/', views.reject_stockin, name='reject_stockin'),

    path('stock', views.stock),
    path('stock_edit/<int:stock_id>', views.stock_edit, name='stock_edit'),
    path('stock_delete/<int:stock_id>', views.stock_delete),

    path('stock_out', views.stock_out),
    path('stockout_add', views.stockout_add),
    path('stockout_edit/<int:id>', views.stockout_edit, name='stockout_edit'),
    path('stockout_delete/<int:id>', views.stockout_delete),
    path('approve_stockout/<int:id>/', views.approve_stockout, name='approve_stockout'),
    path('reject_stockout/<int:id>/', views.reject_stockout, name='reject_stockout'),

    path('item_measurement', views.item_measurement),
    path('item_measurement_add', views.item_measurement_add),
    path('item_measurement_edit/<int:id>', views.item_measurement_edit, name='item_measurement_edit'),
    path('item_measurement_delete/<int:id>', views.item_measurement_delete),

    path('employee', views.employee),
    path('employee_add', views.employee_add),
    path('employee_edit/<int:farm_entity_id>/', views.employee_edit, name='employee_edit'),
    path('employee_delete/<int:farm_entity_id>', views.employee_delete),
    path('employee_view/<str:farm_entity_id>', views.employee_view, name='employee_view'),

    path('department', views.department),
    path('department_add', views.department_add),
    path('department_edit/<int:department_id>', views.department_edit, name='department_edit'),
    path('department_delete/<int:department_id>', views.department_delete),

    path('add_contact', views.add_contact),
    path('add_address', views.add_address),
    path('add_experience', views.add_experience),
    path('add_guarantee', views.add_guarantee),
    path('add_jobhistory', views.add_jobhistory),

    path('milk_production_report/', views.milk_production_report),
    path('stock_report/', views.stock_report),

]