from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index),

    path('cattle', views.cattle),
    path('cattle_add', views.cattle_add),
    path('cattle_view/<str:cattle_id>', views.cattle_view, name='cattle_view'),
    path('cattle_edit/<str:cattle_id>', views.cattle_edit, name='cattle_edit'),
    path('cattle_delete/<str:cattle_id>', views.cattle_delete),

    path('cattle_status', views.cattle_status),
    path('cattle_status_add', views.cattle_status_add),
    path('cattle_status_edit/<str:cattle_status_id>', views.cattle_status_edit, name='cattle_status_edit'),
    path('cattle_status_delete/<str:cattle_status_id>', views.cattle_status_delete),

    path('cattle_breed', views.cattle_breed),
    path('cattle_breed_add', views.cattle_breed_add),
    path('cattle_breed_edit/<str:cattle_breed_id>', views.cattle_breed_edit, name='cattle_breed_edit'),
    path('cattle_breed_delete/<str:cattle_breed_id>', views.cattle_breed_delete),

    path('cattle_pregnancy', views.cattle_pregnancy),
    path('cattle_pregnancy_add', views.cattle_pregnancy_add),
    path('cattle_pregnancy_edit/<str:cattle_pregnancy_id>', views.cattle_pregnancy_edit, name='cattle_pregnancy_edit'),
    path('cattle_pregnancy_delete/<str:cattle_pregnancy_id>', views.cattle_pregnancy_delete),

    path('vaccine', views.vaccine),
    path('vaccine_add', views.vaccine_add),
    path('vaccine_edit/<str:vaccine_id>', views.vaccine_edit, name='vaccine_edit'),
    path('vaccine_delete/<str:vaccine_id>', views.vaccine_delete),

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
    path('shift_edit/<str:shift_id>', views.shift_edit, name='shift_edit'),
    path('shift_delete/<str:shift_id>', views.shift_delete),

    path('job', views.job),
    path('job_add', views.job_add),
    path('job_edit/<str:job_id>', views.job_edit, name='job_edit'),
    path('job_delete/<str:job_id>', views.job_delete),

    path('feed_formulation', views.feed_formulation),
    path('feed_formulation_add', views.feed_formulation_add),
    path('feed_formulation_edit/<str:feed_formulation_id>', views.feed_formulation_edit, name='feed_formulation_edit'),
    path('feed_formulation_delete/<str:feed_formulation_id>', views.feed_formulation_delete),

    # path('item_type', views.item_type),
    # path('item_type_add', views.item_type_add),
    # path('item_type_edit/<str:item_type_id>', views.item_type_edit, name='item_type_edit'),
    # path('item_type_delete/<str:item_type_id>', views.item_type_delete),

    path('item', views.item),
    path('item_add', views.item_add),
    path('item_edit/<str:item_id>', views.item_edit, name='item_edit'),
    path('item_delete/<str:item_id>', views.item_delete),

    path('supplier', views.supplier),
    path('supplier_add', views.supplier_add),
    path('supplier_edit/<str:farm_entity_id>', views.supplier_edit, name='supplier_edit'),
    path('supplier_delete/<str:farm_entity_id>', views.supplier_delete),

    path('request_order', views.request_order),
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
    path('generate_purchase_order/<str:supplier_id>', views.generate_purchase_order, name='generate_purchase_order'),

]