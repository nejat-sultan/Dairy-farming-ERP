from datetime import timedelta
from django.utils import timezone
from .models import Cattle, CattleHasVaccine, DirectlyAddedItem, EmployeeLeave, Order, OrderHasItemSupplier, Stock, Stockout, TaskAssignment
from django.db.models import ExpressionWrapper, FloatField, F
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

def paginate_data(request, queryset, items_per_page):
    paginator = Paginator(queryset, items_per_page)
    page_number = request.GET.get('page')

    try:
        paginated_data = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_data = paginator.page(1)
    except EmptyPage:
        paginated_data = paginator.page(paginator.num_pages)

    return paginated_data

def get_vaccination_notifications():
    notifications  = []
    now = timezone.now()
    one_week_later = now + timedelta(days=7)

    upcoming_vaccinations = CattleHasVaccine.objects.filter(cattle__cattle_status__cattle_status="Active", cattle_given_time__range=(now, one_week_later),given_status='Pending').order_by('cattle_given_time')
    for vaccination in upcoming_vaccinations:
        cattle = vaccination.cattle
        notifications.append({
            'name': cattle.cattle_name,
            'scheduled_time': vaccination.cattle_given_time,
            'vaccine_name': vaccination.vaccine.vaccine_name,  
            'cattle_id': cattle.farm_entity_id,
            'status': 'upcoming'
        })

    overdue_vaccinations = CattleHasVaccine.objects.filter(cattle__cattle_status__cattle_status="Active", cattle_given_time__lt=now,given_status='Pending').order_by('cattle_given_time')
    for vaccination in overdue_vaccinations:
        cattle = vaccination.cattle
        notifications.append({
            'name': cattle.cattle_name,
            'scheduled_time': vaccination.cattle_given_time,
            'vaccine_name': vaccination.vaccine.vaccine_name,
            'cattle_id': cattle.farm_entity_id,
            'status': 'overdue'
        })

    return notifications

def get_low_quantity_items():
    low_quantity_items = Stock.objects.exclude(item__name='Milk').annotate(
        quantity_float=ExpressionWrapper(
            F('quantity'),
            output_field=FloatField()
        )
    ).filter(quantity_float__lt=5)
    return low_quantity_items

# def get_upcoming_due_tasks(employee):
#     now = timezone.now()
#     notification_threshold = now + timedelta(hours=24) 
#     upcoming_due_tasks = TaskAssignment.objects.filter(assigned_to=employee,due_time__lte=notification_threshold,due_time__gt=now).exclude(Q(status='Completed') | Q(status='Reassigned'))
#     return upcoming_due_tasks

def get_overdue_tasks(employee=None):
    now = timezone.now()
    if employee:
        overdue_tasks = TaskAssignment.objects.filter(assigned_to=employee, due_time__lt=now, status__in=['pending', 'On Progress'])
    else:
        overdue_tasks = TaskAssignment.objects.filter(due_time__lt=now, status__in=['pending', 'On Progress'])
    return overdue_tasks


def get_assigned_tasks(employee):
    assigned_tasks = TaskAssignment.objects.filter(assigned_to=employee, status='pending').order_by('-due_time')
    return assigned_tasks

def get_completed_tasks():
    completed_tasks = TaskAssignment.objects.filter(Q(status='Completed') | Q(status='Reassigned'),approval_status='pending')
    return completed_tasks

def get_rejected_tasks(employee):
    rejected_tasks = TaskAssignment.objects.filter(assigned_to=employee,approval_status='Rejected')
    return rejected_tasks

def get_approval_required_orders():
    approval_required_orders = Order.objects.filter(request_approved='Pending')
    return approval_required_orders

def get_approval_required_ordersuppliers():
    approval_required_ordersuppliers = OrderHasItemSupplier.objects.filter(status='Pending')
    return approval_required_ordersuppliers

def get_approval_required_leave_requests():
    approval_required_leave_requests = EmployeeLeave.objects.filter(approval_status='Pending')
    return approval_required_leave_requests

# def get_approved_leave(employee):
#     approved_leave = EmployeeLeave.objects.filter(person_farm_entity_id=employee,approval_status='Approved')
#     return approved_leave

def get_approval_required_stockout_requests():
    approval_required_stockout_requests = Stockout.objects.filter(status='Pending')
    return approval_required_stockout_requests

def get_approval_required_stockin_requests():
    approval_required_stockin_requests = DirectlyAddedItem.objects.filter(approval_status='Pending')
    return approval_required_stockin_requests