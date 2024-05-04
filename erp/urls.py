from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index),
    path('request_order', views.request_order),
    path('add_orderRequest', views.add_orderRequest),

    path('cattle', views.cattle),
    path('cattle_add', views.cattle_add),
    path('cattle_view/<str:cattle_id>', views.cattle_view, name='cattle_view'),
    path('cattle_edit/<str:cattle_id>', views.cattle_edit, name='cattle_edit'),
    path('cattle_delete/<str:cattle_id>', views.cattle_delete),

    path('cattle_status', views.cattle_status),
    path('cattle_status_add', views.cattle_status_add),
    path('cattle_status_edit/<str:cattle_status_id>', views.cattle_status_edit, name='cattle_status_edit'),
    path('cattle_status_delete/<str:cattle_status_id>', views.cattle_status_delete),

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
    
]