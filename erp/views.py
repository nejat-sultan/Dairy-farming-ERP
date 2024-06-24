import base64
from collections import defaultdict
from datetime import datetime
from django.utils.timezone import now, timedelta
import json
import logging
import os
import io

import matplotlib # type: ignore
matplotlib.use('agg') 
import matplotlib.pyplot as plt # type: ignore
import pandas as pd # type: ignore
from django.forms import DateField, ValidationError
from django.shortcuts import get_object_or_404, render,redirect
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from decimal import Decimal
from erp.decorators import allowed_users, unauthenticated_user
from testproject import settings
from .models import CattleBreed, CattleHasFeed, CattleHasVaccine, CattleHealthCheckup, CattleHealthCheckupHasMedicine, CattlePhoto, CattlePregnancy, CattleStatus, ContactType, Customer, Dashboard, Department, DirectlyAddedItem, Employee, EmployeeExperience, EmployeeLeave, Farm, FarmContacts, FarmEntity, FarmEntityAddress, FarmEntityContact, FeedFormulation, FeedIngredient, Guarantee, GuaranteeType, HealthCheckupSymptoms, Item, ItemType, OtherIncomeExpense, PaymentMethod, SalesOrder, Stock, ItemMeasurement, Job, JobHistory, Medicine, MilkProduction, Order, OrderHasItem, OrderHasItemSupplier, Person, PersonTitle, PersonType, PregnancyStatus, Region, Shift, Stockout, Supplier, SupplierType, Task, TaskAssignment, UserProfile, Vaccine
from .models import Cattle
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, GroupAssignmentForm, GroupCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.models import User, Group, Permission
from django.utils.dateparse import parse_date
from django.http import JsonResponse
from django.db import transaction
from django.db.models import Sum, F, FloatField
from django.db.models.functions import Cast
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import permission_required
from django.contrib.auth import update_session_auth_hash
from .utils import get_low_quantity_items, get_overdue_vaccines, paginate_data 

def get_latest_farm():
    return Farm.objects.last()

@login_required(login_url='login')
def farm(request):
    if not request.user.has_perm('erp.add_farm'):
        return HttpResponse('You are not authorised to view this page', status=403)
    
    latest_farm = get_latest_farm()

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        nick_name = request.POST.get('nick_name')
        country = request.POST.get('country')
        region_id = request.POST.get('region_id')
        house_number = request.POST.get('house_number')
        kebele = request.POST.get('kebele')
        woreda = request.POST.get('woreda')
        zone_subcity = request.POST.get('zone_subcity')
        date = timezone.now().date()
        
        if 'logo_photo' in request.FILES:
            photo_file = request.FILES['logo_photo']
            fs = FileSystemStorage(location=settings.MEDIA_ROOT + '/photos')
            filename = fs.save(photo_file.name, photo_file)
            logo_photo_url = settings.MEDIA_URL + 'photos/' + filename

        else:
            logo_photo_url = None
        
        if latest_farm:
            latest_farm.full_name = full_name
            latest_farm.nick_name = nick_name
            latest_farm.country = country
            latest_farm.region_id = region_id
            latest_farm.house_number = house_number
            latest_farm.kebele = kebele
            latest_farm.woreda = woreda
            latest_farm.zone_subcity = zone_subcity
            latest_farm.modified_date = date
            if logo_photo_url:
                latest_farm.logo_url = logo_photo_url

            latest_farm.save()
            messages.success(request, "Farm Updated Successfully!")
        else:
            Farm.objects.create(full_name=full_name,logo_url=logo_photo_url, nick_name=nick_name, country=country, region_id=region_id, house_number=house_number, kebele=kebele, woreda=woreda, zone_subcity=zone_subcity, modified_date=date)
            messages.success(request, "Farm Added Successfully!")

        return redirect('farm')
    
    region_data = Region.objects.all()
    farm_contacts = FarmContacts.objects.all()
    context = {'latest_farm': latest_farm, 'farm_contacts': farm_contacts, 'data1': region_data}

    return render(request, 'company/farm.html', context)

def farm_context_processor(request):
    latest_farm = get_latest_farm()
    overdue_cattle = get_overdue_vaccines()
    low_quantity_items = get_low_quantity_items()
    notifications = {
        'overdue_cattle': overdue_cattle,
        'low_quantity_items': low_quantity_items,
    }
    total_notifications = len(overdue_cattle) + len(low_quantity_items)

    return {
        'latest_farm': latest_farm,
        'notifications': notifications,
        'total_notifications': total_notifications,
        'overdue_count': len(overdue_cattle),
        'low_quantity_count': len(low_quantity_items),
    }


@login_required(login_url='login')
def farm_contact_add(request):
    if not request.user.has_perm('erp.add_farmcontacts'):
        return HttpResponse('You are not authorised to view this page', status=403)
    
    if request.method == "POST":
        cfarm_id = request.POST.get('farm_id')
        ccontact_type_id = request.POST.get('contact_type_id')
        ccontact = request.POST.get('contact')

        query = FarmContacts(farm_id=cfarm_id, contact_type_id=ccontact_type_id, contact=ccontact)
        query.save()
        messages.success(request, "Farm Contact Added Successfully!")
        return redirect("farm")
    
    farm_data = Farm.objects.all()
    type_data = ContactType.objects.all()
    context = {
        'data1': farm_data,
        'data2': type_data,
    }
    return render(request, 'company/farm_contact_add.html', context)

@login_required(login_url='login')
def farm_contact_edit(request, id):
    if not request.user.has_perm('erp.change_farmcontacts'):
        return HttpResponse('You are not authorised to view this page', status=403)
    edit = FarmContacts.objects.get(id=id)
    if request.method == "POST":
        cfarm_id = request.POST.get('farm_id')
        ccontact_type_id = request.POST.get('contact_type_id')
        ccontact = request.POST.get('contact')

        edit.farm_id = cfarm_id
        edit.contact_type_id = ccontact_type_id
        edit.contact = ccontact

        edit.save()
        messages.warning(request, "Farm Contact Updated Successfully!")
        return redirect("/farm")
        
    
    farm_data = Farm.objects.all()
    type_data = ContactType.objects.all()
    context = {
        "farm": edit,
        'data1': farm_data,
        'data2': type_data,
    }
    
    return render(request, 'company/farm_contact_edit.html', context)

@login_required(login_url='login')
def farm_contact_delete(request, id):
    if not request.user.has_perm('erp.delete_farmcontacts'):
        return HttpResponse('You are not authorised to view this page', status=403)
    d = FarmContacts.objects.get(id=id)
    d.delete()
    messages.error(request, "Farm Contact Deleted Successfully!")
    return redirect("/farm")


@login_required(login_url='login')
def user(request):
    if not request.user.has_perm('auth.view_user'):
        return HttpResponse('You are not authorised to view this page', status=403)
    user_profiles = UserProfile.objects.select_related('user', 'employee').all()
    context = {
        'user_profiles': user_profiles,
    }
    return render(request, 'auth/user.html', context)

@login_required(login_url='login')
def register(request):
    if not request.user.has_perm('auth.add_user'):
        return HttpResponse('You are not authorised to view this page', status=403)
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            employee_id = form.cleaned_data.get('employee_id')

            user_profile = UserProfile.objects.create(
                user=user,
                employee_id=employee_id
            )

            messages.success(request, "User registered Successfully!")
            return redirect("/user") 

    context = {'form': form}
    return render(request, 'auth/register.html', context)

@login_required(login_url='login')
def edit_user(request, user_id):
    if not request.user.has_perm('auth.change_user'):
       return HttpResponse('You are not authorised to view this page', status=403)
    user_profile = get_object_or_404(UserProfile, user_id=user_id)
    user = user_profile.user
    employees = Employee.objects.select_related('person_farm_entity').all()

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        employee_id = request.POST.get('employee_id')
        
        if username:
            user.username = username
        if email:
            user.email = email
        user.save()

        if employee_id:
            try:
                employee = Employee.objects.get(person_farm_entity=employee_id)
                user_profile.employee = employee
                user_profile.save()
            except Employee.DoesNotExist:
                messages.error(request, "Selected employee does not exist.")
        
        messages.success(request, "User profile updated successfully!")
        return redirect("/user") 

    context = {
        'user_profile': user_profile,
        'employees': employees,
    }

    return render(request, 'auth/edit_user.html', context)


def user_delete(request, id):
    if not request.user.has_perm('auth.delete_user'):
        return HttpResponse('You are not authorised to view this page', status=403)
    try:
        user = User.objects.get(pk=id)
        user_profile = user.userprofile
        user_profile.delete()
        user.delete()
        
        messages.success(request, "User deleted successfully!")
    except User.DoesNotExist:
        messages.error(request, "User not found!")
    
    return redirect("/user")

@login_required(login_url='login')
def group(request):
    if not request.user.has_perm('auth.view_group'):
        return HttpResponse('You are not authorised to view this page', status=403)
    groups = Group.objects.all()
    context = {"groups":groups}
    return render(request, 'auth/group.html', context)

@login_required(login_url='login')
def create_group(request):
    if not request.user.has_perm('auth.add_group'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method == 'POST':
        form = GroupCreationForm(request.POST)
        if form.is_valid():
            group = form.save()
            group.permissions.set(form.cleaned_data['permissions'])
            return redirect('group') 
    else:
        form = GroupCreationForm()
    return render(request, 'auth/create_group.html', {'form': form})

@login_required(login_url='login')
def edit_group(request, id):
    if not request.user.has_perm('auth.change_group'):
        return HttpResponse('You are not authorised to view this page', status=403)
    group = get_object_or_404(Group, id=id)
    all_permissions = Permission.objects.all()  
    assigned_permissions = group.permissions.all() 
    
    if request.method == 'POST':
        name = request.POST.get('name')
        selected_permissions = request.POST.getlist('permissions')
        
        if name:
            group.name = name
            group.save()
        
        group.permissions.clear()
        for permission_id in selected_permissions:
            permission = Permission.objects.get(id=permission_id)
            group.permissions.add(permission)
        
        messages.success(request, "Group updated successfully!")
        return redirect("/group")

    context = {
        'group': group, 
        'all_permissions': all_permissions,
        'assigned_permissions': assigned_permissions
    }
    return render(request, 'auth/edit_group.html', context)
    
def group_delete(request, id):
    if not request.user.has_perm('auth.delete_group'):
        return HttpResponse('You are not authorised to view this page', status=403)
    d = Group.objects.get(id=id)
    d.delete()
    messages.error(request, "Role Deleted Successfully!")
    return redirect("/group")

@login_required(login_url='login')
def assign_users_to_group(request, user_id):
    user = User.objects.get(id=user_id)
    groups = Group.objects.all() 
    
    if request.method == 'POST':
        group_id = request.POST.get('group')  
        group = Group.objects.get(id=group_id)
        user.groups.clear()  
        user.groups.add(group)  
        return redirect('user')  
    
    return render(request, 'auth/assign_users_to_group.html', {'user': user, 'groups': groups})


@unauthenticated_user
def login_page(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/index")
        else:
            messages.error(request, "Username or password is incorrect!")
            return render(request, 'auth/login.html')
        
    hashed_password = make_password('admin@admin')
    print(hashed_password)
    
    context = {}
    return render(request, 'auth/login.html', context)


def logout_user(request):
    logout(request)
    return redirect("/login")

@login_required(login_url='login')
def profile(request):
    user = request.user
    try:
        user_profile = UserProfile.objects.get(user=user)
        employee = Employee.objects.get(pk=user_profile.employee_id)
        person = Person.objects.get(pk=employee.person_farm_entity_id)
        farm_entity = person.farm_entity

        experience = EmployeeExperience.objects.filter(person_farm_entity=employee)
        contact = FarmEntityContact.objects.filter(farm_entity=farm_entity)
        address = FarmEntityAddress.objects.filter(farm_entity=farm_entity)
        guarantee = Guarantee.objects.filter(person_farm_entity=employee)
        jobhistory = JobHistory.objects.filter(person_farm_entity=employee)

        context = {
            'person': person,
            'employee': employee,
            'farm_entity': farm_entity,
            'experience': experience,
            'contact': contact,
            'address': address,
            'jobhistory': jobhistory,
            'guarantee': guarantee,
        }

    except UserProfile.DoesNotExist:
        context = {}

    except Employee.DoesNotExist:
        context = {}

    except Person.DoesNotExist:
        context = {}

    return render(request, 'auth/profile.html', context)

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        user = request.user

        if not user.check_password(old_password):
            messages.error(request, 'Old password is incorrect')
            return redirect('change_password')

        if new_password1 != new_password2:
            messages.error(request, 'New passwords do not match')
            return redirect('change_password')

        user.set_password(new_password1)
        user.save()

        update_session_auth_hash(request, user)

        messages.success(request, 'Password changed successfully')
        return redirect('index')
    
    return render(request, 'auth/change_password.html')

@login_required(login_url='login')
def index(request):
#milk production report
    end_date = now()
    start_date = end_date - timedelta(days=15)
    # Query MilkProduction data for the last week
    milk_data = MilkProduction.objects.filter(milk_time__range=(start_date, end_date)).order_by('milk_time')
    # Process the data into a DataFrame
    df = pd.DataFrame(list(milk_data.values('milk_time', 'amount_in_liter')))
    # Resample data to daily totals
    if not df.empty:
        df['milk_time'] = pd.to_datetime(df['milk_time'])
        df.set_index('milk_time', inplace=True)
        daily_data = df.resample('D').sum()

        labels = [date.strftime('%Y-%m-%d') for date in daily_data.index]
        data = list(daily_data['amount_in_liter'])
    else:
        labels = []
        data = []

    chart_data = {
        'labels': labels,
        'datasets': [{
            'label': 'Daily Milk Production (Liters)',
            'data': data,
            'backgroundColor': '#007f5c',
            'borderColor': '#007f5c',
            'borderWidth': 1,
            'fill': False
        }]
    }
    chart_data_json = json.dumps(chart_data)

#stock report
    stock_data = Stock.objects.all()
    stock_dict = defaultdict(float)
    
    for stock in stock_data:
        item_name = stock.item.name
        quantity = float(stock.quantity)
        stock_dict[item_name] += quantity

    labels = list(stock_dict.keys())
    quantities = list(stock_dict.values())

    chart_data2 = {
        'labels': labels,
        'datasets': [{
            'label': 'Quantity in Stock',
            'data': quantities,
            'backgroundColor': 'rgba(0, 127, 92, 0.2)',
            'borderColor': '#007f5c',
            'borderWidth': 1
        }]
    }
    chart_data_json2 = json.dumps(chart_data2)

    #vaccination report
    total_cattle_count = Cattle.objects.count()

    # Get vaccinated cattle count
    vaccinated_cattle_count = CattleHasVaccine.objects.values('cattle').distinct().count()

    # Calculate non-vaccinated cattle count
    non_vaccinated_cattle_count = total_cattle_count - vaccinated_cattle_count

    # Prepare the data for the chart
    chart_data3 = {
        'labels': ['Vaccinated', 'Non-Vaccinated'],
        'datasets': [{
            'data': [vaccinated_cattle_count, non_vaccinated_cattle_count],
            'backgroundColor': ['rgba(0, 127, 92, 0.2)','rgba(255, 99, 132, 0.2)'],
            'borderColor': ['rgba(0, 127, 92, 1)','rgba(255, 99, 132, 1)'],
            'borderWidth': 1
        }]
    }
    chart_data_json3 = json.dumps(chart_data3)
    

    dash1 = Dashboard()
    dash1.amount =  OrderHasItemSupplier.objects.filter(status='approved').count()
    dash1.description = 'Purchase Orders'

    dash2 = Dashboard()
    dash2.amount = Stock.objects.all().count()
    dash2.description = 'Stock Available'

    dash3 = Dashboard()
    dash3.amount = 0
    dash3.description = 'Sales'

    dash4 = Dashboard()
    dash4.amount = User.objects.count()
    dash4.description = 'System Users'

    dash5 = Dashboard()
    dash5.amount = Supplier.objects.all().count()
    dash5.description = 'Supplier'

    dash6 = Dashboard()
    dash6.amount = Employee.objects.all().count()
    dash6.description = 'Employees'

    dash7 = Dashboard()
    dash7.amount = 0
    dash7.description = 'Customers'

    data = OrderHasItem.objects.all()[:10]
    orderdatas = Order.objects.all()
    item_data = Item.objects.all()
    cattle = Cattle.objects.all()[:10]
    # photos = CattlePhoto.objects.all()
    breeds = CattleBreed.objects.all()
    stocks = Stock.objects.all()
    employeedatas = Person.objects.all()[:10]
    healthdatas = CattleHealthCheckup.objects.all()[:10]
    cattlepregnancy = CattlePregnancy.objects.all()[:10]

    current_user = request.user
    user_profile = UserProfile.objects.get(user=current_user)
    current_employee = user_profile.employee

    leave = EmployeeLeave.objects.filter(person_farm_entity_id=current_employee)[:10]
    task = TaskAssignment.objects.filter(assigned_to=current_employee)[:10]

    overdue_cattle = get_overdue_vaccines()
    low_quantity_items = get_low_quantity_items()
    total_notifications = len(overdue_cattle) + len(low_quantity_items)
 
    cattle_photos = {}
    for cow in cattle:
        photo = CattlePhoto.objects.filter(cattle=cow).first()
        cattle_photos[cow.farm_entity_id] = photo.cattle_photo_url if photo else None

    print("Cattle Photos Dictionary:", cattle_photos)  

    context = {
        # 'plot_img_base64': plot_img_base64,
        'chart_data_json': chart_data_json,
        'chart_data_json2': chart_data_json2,
        'chart_data_json3': chart_data_json3,
        'dash1': dash1, 
        'dash2': dash2, 
        'dash3': dash3, 
        'dash4': dash4,
        'dash5': dash5, 
        'dash6': dash6, 
        'dash7': dash7,

        'stocks':stocks,

        "data1":data,'orderdatas': orderdatas,'item_data': item_data,
        'cattle': cattle,'cattle_photos': cattle_photos,'breeds': breeds, 
        'employeedatas':employeedatas,'healthdatas':healthdatas,'cattlepregnancy':cattlepregnancy,'leave':leave,'task':task,
        'overdue_cattle': overdue_cattle,'low_quantity_items': low_quantity_items, 
    }
    return render(request, 'index.html',context)

@login_required(login_url='login')
def cattle(request):
    if not request.user.has_perm('erp.view_cattle'):
        return HttpResponse('You are not authorised to view this page', status=403)
    data = Cattle.objects.all()
    paginated_data = paginate_data(request, data, 10) 
    context = {"data":paginated_data}

    return render(request, 'cattle/cattle.html', context)

@login_required(login_url='login')
def cattle_view(request, farm_entity_id):
    if not request.user.has_perm('erp.view_cattle'):
        return HttpResponse('You are not authorised to view this page', status=403)
    cattle = get_object_or_404(Cattle, farm_entity_id=farm_entity_id)
    photos = CattlePhoto.objects.filter(cattle=cattle)
    breeds = CattleBreed.objects.filter(cattle=cattle)
    statuses = CattlePregnancy.objects.filter(cattle=cattle).order_by('-cattle_id').first()
    
    productions = MilkProduction.objects.filter(cattle=cattle).order_by('-milk_time')[:5]
    vaccinations = CattleHasVaccine.objects.filter(cattle=cattle).order_by('-cattle_given_time')[:5]
    healths = CattleHealthCheckup.objects.filter(cattle=cattle).order_by('-cattle_id')[:5]
    symptoms = HealthCheckupSymptoms.objects.filter(cattle_health_checkup__in=healths).order_by('-modified_date')[:5]
    medicines = CattleHealthCheckupHasMedicine.objects.filter(cattle_health_checkup__in=healths).order_by('-modified_date')[:5]
    feeds = CattleHasFeed.objects.filter(cattle_farm_entity=cattle).order_by('-feed_time')[:5]
    
    
    context = {
        'cattle': cattle,
        'photos': photos,
        'breeds': breeds,
        'statuses': statuses,
        'productions': productions,
        'vaccinations': vaccinations,
        'healths': healths,
        'symptoms': symptoms,
        'medicines': medicines,
        'feeds': feeds,
    }

    return render(request, 'cattle/cattle_view.html', context)


@login_required(login_url='login')
def cattle_add(request):
    if not request.user.has_perm('erp.add_cattle'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method == "POST":
        cid = request.POST.get('id')
        cdob = request.POST.get('dob')
        cname = request.POST.get('name')
        cgender = request.POST.get('gender')
        cfather = request.POST.get('father')
        cmother = request.POST.get('mother')
        cestimatedprice = request.POST.get('estimated_price')
        cbreed = request.POST.get('breed')
        cstatus = request.POST.get('status')
        cacquired_status = request.POST.get('acquired_status')
        cacquired_date = request.POST.get('acquired_date')

        farm_entity = FarmEntity.objects.create(modified_date=timezone.now())

        errors = []
        if not cid:
            errors.append('Cattle ID is required.')

        if cdob:
            try:
                cdob = datetime.strptime(cdob, '%Y-%m-%dT%H:%M')
            except ValueError:
                errors.append('Date of Birth must be in YYYY-MM-DDTHH:MM format.')
        else:
            cdob = None 

        if cestimatedprice:
            try:
                cestimatedprice = float(cestimatedprice)
                if cestimatedprice <= 0:
                    errors.append("Price must be a positive number.")
            except ValueError:
                errors.append('Estimated price must be a number.')
        else:
            cestimatedprice = None 

        if cacquired_date:
            try:
                cacquired_date = datetime.strptime(cacquired_date, '%Y-%m-%dT%H:%M')
            except ValueError:
                errors.append('Acquired date must be in YYYY-MM-DDTHH:MM format.')
        else:
            cacquired_date = None 

        if errors:
            context = {
                'errors': errors,
                'data1': CattleStatus.objects.all(),
                'data2': Cattle.objects.all(),
                'data3': CattleBreed.objects.all(),
            }
            return render(request, 'cattle/cattle_add.html', context)
        
        query = Cattle(farm_entity=farm_entity,cattle_ear_id=cid, cattle_date_of_birth=cdob, cattle_name=cname, cattle_gender=cgender, father_id=cfather, mother_id=cmother, estimated_price=cestimatedprice, cattle_breed_id=cbreed, cattle_status_id=cstatus, acquired_status=cacquired_status, acquired_date=cacquired_date)
        query.save()
        messages.success(request, "Cattle Added Successfully!")
        return redirect("/cattle")

    breed_data = CattleBreed.objects.all()
    data = CattleStatus.objects.all()
    cattle_data = Cattle.objects.all()
    father_data = Cattle.objects.filter(cattle_gender="Male")
    mother_data = Cattle.objects.filter(cattle_gender="Female")

    context = {
        'data1': data,
        'data2': cattle_data,
        'data3': breed_data,
        'data4': father_data,
        'data5': mother_data,
    }

    return render(request, 'cattle/cattle_add.html', context)

@login_required(login_url='login')
def cattle_edit(request,farm_entity_id):
    if not request.user.has_perm('erp.change_cattle'):
        return HttpResponse('You are not authorised to view this page', status=403)
    edit = Cattle.objects.get(farm_entity_id=farm_entity_id)
    
    if request.method == "POST":
        cid=request.POST.get('id')
        cdob=request.POST.get('dob')
        cname=request.POST.get('name')
        cgender=request.POST.get('gender')
        cfather = request.POST.get('father')
        cmother = request.POST.get('mother')
        cestimatedprice=request.POST.get('estimated_price')
        cbreed=request.POST.get('breed')
        cstatus=request.POST.get('status')
        cacquired_status = request.POST.get('acquired_status')
        cacquired_date = request.POST.get('acquired_date')

        errors = []
        if not cid:
            errors.append('Cattle ID is required.')

        if cdob:
            try:
                cdob = datetime.strptime(cdob, '%Y-%m-%dT%H:%M')
            except ValueError:
                errors.append('Date of Birth must be in YYYY-MM-DDTHH:MM format.')
        else:
            cdob = None 

        if cestimatedprice:
            try:
                cestimatedprice = float(cestimatedprice)
                if cestimatedprice <= 0:
                    errors.append("Price must be a positive number.")
            except ValueError:
                errors.append('Estimated price must be a number.')
        else:
            cestimatedprice = None 

        if cacquired_date:
            try:
                cacquired_date = datetime.strptime(cacquired_date, '%Y-%m-%dT%H:%M')
            except ValueError:
                errors.append('Acquired date must be in YYYY-MM-DDTHH:MM format.')
        else:
            cacquired_date = None 

        if errors:
            context = {
                'cattle': edit,
                'errors': errors,
                'cattle_statuses': CattleStatus.objects.all(),
                'cattle_breed': CattleBreed.objects.all(),
                'data2': Cattle.objects.all()
            }
            return render(request, 'cattle/cattle_edit.html', context)

        edit.cattle_ear_id = cid
        edit.cattle_date_of_birth = cdob
        edit.cattle_name = cname
        edit.cattle_gender = cgender
        edit.father_id = cfather
        edit.mother_id = cmother
        edit.estimated_price = cestimatedprice
        edit.cattle_breed_id = cbreed
        edit.cattle_status_id = cstatus
        edit.acquired_status = cacquired_status
        edit.acquired_date = cacquired_date

        edit.save()
        messages.warning(request, "Cattle Updated Successfully!")
        return redirect("/cattle")
        
    
    # d = Cattle.objects.get(farm_entity_id=farm_entity_id)
    cattle_statuses = CattleStatus.objects.all()
    cattle_breed = CattleBreed.objects.all()
    cattle_data = Cattle.objects.all()
    father_data = Cattle.objects.filter(cattle_gender="Male")
    mother_data = Cattle.objects.filter(cattle_gender="Female")
    
    context = {"cattle": edit, "cattle_statuses": cattle_statuses, "cattle_breed": cattle_breed, 'data2': cattle_data,  'data4': father_data,'data5': mother_data,}

    return render(request, 'cattle/cattle_edit.html', context)


def cattle_delete(request, farm_entity_id):
    if not request.user.has_perm('erp.delete_cattle'):
        return HttpResponse('You are not authorised to view this page', status=403)
    d = Cattle.objects.get(farm_entity_id=farm_entity_id)
    d.delete()
    messages.error(request, "Cattle Deleted Successfully!")
    return redirect("/cattle")


def add_photo(request):
    if not request.user.has_perm('erp.add_cattlephoto'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method == 'POST':
        cattle_id = request.POST.get('cattle_id')
        photo_description = request.POST.get('photo_description')


        if 'photo_url' in request.FILES:
            photo_file = request.FILES['photo_url']

            fs = FileSystemStorage(location=settings.MEDIA_ROOT + '/photos')
            filename = fs.save(photo_file.name, photo_file)
            photo_url = settings.MEDIA_URL + 'photos/' + filename
            

            photo = CattlePhoto(
                cattle_id=cattle_id,
                cattle_photo_url=photo_url,
                cattle_photo_description=photo_description
            )
            photo.save()

            messages.success(request, "Cattle Photo Added Successfully!")
            return redirect("/cattle")
        
    data = CattleStatus.objects.all()
    cattle_data = Cattle.objects.all()

    context = {
        'data1': data,
        'data2': cattle_data,
    }

    return render(request, 'cattle/cattle_add.html', context)

@login_required(login_url='login')
def cattle_status(request):
    if not request.user.has_perm('erp.view_cattlestatus'):
        return HttpResponse('You are not authorised to view this page', status=403)
    data = CattleStatus.objects.all()
    paginated_data = paginate_data(request, data, 10) 
    context = {"data1":paginated_data}

    return render(request, 'cattle/cattle_status.html', context)

@login_required(login_url='login')
def cattle_status_add(request):
    if not request.user.has_perm('erp.add_cattlestatus'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method=="POST":
        cstatus=request.POST.get('status')
        cdate = datetime.now().date()

        query = CattleStatus(cattle_status=cstatus, modified_date=cdate)
        query.save()
        messages.success(request, "Cattle Status Added Successfully!")
        return redirect("/cattle_status")

    return render(request, 'cattle/cattle_status_add.html')

@login_required(login_url='login')
def cattle_status_edit(request,cattle_status_id):
    if not request.user.has_perm('erp.change_cattlestatus'):
        return HttpResponse('You are not authorised to view this page', status=403)
    edit = CattleStatus.objects.get(cattle_status_id=cattle_status_id)
    
    if request.method == "POST":
        cstatus=request.POST.get('status')
        cdate = datetime.now().date()
        
        edit.cattle_status = cstatus
        edit.modified_date = cdate
        edit.save()
        messages.warning(request, "Cattle Status Updated Successfully!")
        return redirect("/cattle_status")

    d = CattleStatus.objects.get(cattle_status_id=cattle_status_id)
    context = {"d": d}

    return render(request, 'cattle/cattle_status_edit.html', context)

@login_required(login_url='login')
def cattle_status_delete(request, cattle_status_id):
    if not request.user.has_perm('erp.delete_cattlestatus'):
        return HttpResponse('You are not authorised to view this page', status=403)
    d = CattleStatus.objects.get(cattle_status_id=cattle_status_id)
    d.delete()
    messages.error(request, "Cattle Status Deleted Successfully!")
    return redirect("/cattle_status")

@login_required(login_url='login')
def cattle_breed(request):
    if not request.user.has_perm('erp.view_cattlebreed'):
        return HttpResponse('You are not authorised to view this page', status=403)
    data = CattleBreed.objects.all()
    paginated_data = paginate_data(request, data, 10) 
    context = {"data1":paginated_data}

    return render(request, 'cattle/cattle_breed.html', context)

@login_required(login_url='login')
def cattle_breed_add(request):
    if not request.user.has_perm('erp.add_cattlebreed'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method=="POST":
        cbreed_type=request.POST.get('breed_type')
        cbreed_description=request.POST.get('breed_description')
        cdate = datetime.now().date()

        query = CattleBreed(cattle_breed_type=cbreed_type, cattle_breed_description=cbreed_description, modified_date=cdate)
        query.save()
        messages.success(request, "Cattle Breed Added Successfully!")
        return redirect("/cattle_breed")

    return render(request, 'cattle/cattle_breed_add.html')

@login_required(login_url='login')
def cattle_breed_edit(request,cattle_breed_id):
    if not request.user.has_perm('erp.change_cattlebreed'):
        return HttpResponse('You are not authorised to view this page', status=403)
    edit = CattleBreed.objects.get(cattle_breed_id=cattle_breed_id)
    
    if request.method == "POST":
        cbreed_type=request.POST.get('breed_type')
        cbreed_description=request.POST.get('breed_description')
        cdate = datetime.now().date()
        
        edit.cattle_breed_type = cbreed_type
        edit.cattle_breed_description = cbreed_description
        edit.modified_date = cdate
        
        edit.save()
        messages.warning(request, "Cattle Breed Updated Successfully!")
        return redirect("/cattle_breed")

    d = CattleBreed.objects.get(cattle_breed_id=cattle_breed_id)
    context = {"d": d}

    return render(request, 'cattle/cattle_breed_edit.html', context)

def cattle_breed_delete(request, cattle_breed_id):
    if not request.user.has_perm('erp.delete_cattlebreed'):
        return HttpResponse('You are not authorised to view this page', status=403)
    d = CattleBreed.objects.get(cattle_breed_id=cattle_breed_id)
    d.delete()
    messages.error(request, "Cattle Breed Deleted Successfully!")
    return redirect("/cattle_breed")

@login_required(login_url='login')
def pregnancy_status(request):
    if not request.user.has_perm('erp.view_pregnancystatus'):
        return HttpResponse('You are not authorised to view this page', status=403)
    data = PregnancyStatus.objects.all()
    paginated_data = paginate_data(request, data, 10) 
    context = {"data1":paginated_data}

    return render(request, 'cattle/pregnancy_status.html', context)

@login_required(login_url='login')
def pregnancy_status_add(request):
    if not request.user.has_perm('erp.add_pregnancystatus'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method=="POST":
        cstatus=request.POST.get('status')
        cdate = datetime.now().date()

        query = PregnancyStatus(pregnancy_status=cstatus, modified_date=cdate)
        query.save()
        messages.success(request, "Pregnancy Status Added Successfully!")
        return redirect("/pregnancy_status")

    return render(request, 'cattle/pregnancy_status_add.html')

@login_required(login_url='login')
def pregnancy_status_edit(request,pregnancy_status_id):
    if not request.user.has_perm('erp.change_pregnancystatus'):
        return HttpResponse('You are not authorised to view this page', status=403)
    edit = PregnancyStatus.objects.get(pregnancy_status_id=pregnancy_status_id)
    
    if request.method == "POST":
        cstatus=request.POST.get('status')
        cdate = datetime.now().date()
        
        edit.pregnancy_status = cstatus
        edit.modified_date = cdate
        edit.save()
        messages.warning(request, "Pregnancy Status Updated Successfully!")
        return redirect("/pregnancy_status")

    d = PregnancyStatus.objects.get(pregnancy_status_id=pregnancy_status_id)
    context = {"d": d}

    return render(request, 'cattle/pregnancy_status_edit.html', context)

@login_required(login_url='login')
def pregnancy_status_delete(request, pregnancy_status_id):
    if not request.user.has_perm('erp.delete_pregnancystatus'):
        return HttpResponse('You are not authorised to view this page', status=403)
    d = PregnancyStatus.objects.get(pregnancy_status_id=pregnancy_status_id)
    d.delete()
    messages.error(request, "Pregnancy Status Deleted Successfully!")
    return redirect("/pregnancy_status")


@login_required(login_url='login')
def cattle_pregnancy(request):
    if not request.user.has_perm('erp.view_cattlepregnancy'):
        return HttpResponse('You are not authorised to view this page', status=403)
    data = CattlePregnancy.objects.all()
    cattle = Cattle.objects.all()

    paginated_data = paginate_data(request, data, 10) 
    context = {"data1":paginated_data, 'cattle': cattle,}

    return render(request, 'cattle/cattle_pregnancy.html', context)

@login_required(login_url='login')
def cattle_pregnancy_add(request):
    if not request.user.has_perm('erp.add_cattlepregnancy'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method=="POST":
        cpregnancy_type=request.POST.get('pregnancy_type')
        cpregnancy_date=request.POST.get('pregnancy_date')
        ccattle_id=request.POST.get('cattle_id')
        cpregnancy_status = request.POST.get('pregnancy_status')

        errors = []

        if cpregnancy_date:
            parsed_pregnancy_date = parse_date(cpregnancy_date)
            if not parsed_pregnancy_date:
                errors.append('Pregnancy date must be in YYYY-MM-DD format.')
            else:
                cpregnancy_date = parsed_pregnancy_date
        else:
            errors.append('Pregnancy date is required.')

        if not cpregnancy_type:
            errors.append('Pregnancy type is required.')

        if errors:
            context = {
                'errors': errors,
                'data1': Cattle.objects.all(),
                'data2': PregnancyStatus.objects.all(),
            }
            return render(request, 'cattle/cattle_pregnancy_add.html', context)

        query = CattlePregnancy(cattle_pregnancy_type=cpregnancy_type, cattle_pregnancy_date=cpregnancy_date, cattle_id=ccattle_id, pregnancy_status_id=cpregnancy_status)
        query.save()
        messages.success(request, "Cattle Pregnancy Added Successfully!")
        return redirect("/cattle_pregnancy")
    
    cattle_data = Cattle.objects.filter(cattle_gender="Female")
    status_data = PregnancyStatus.objects.all()

    context = {
        'data1': cattle_data,
        'data2': status_data,
    }

    return render(request, 'cattle/cattle_pregnancy_add.html', context)

@login_required(login_url='login')
def cattle_pregnancy_edit(request,cattle_pregnancy_id):
    if not request.user.has_perm('erp.change_cattlepregnancy'):
        return HttpResponse('You are not authorised to view this page', status=403)
    edit = CattlePregnancy.objects.get(cattle_pregnancy_id=cattle_pregnancy_id)
    
    if request.method == "POST":
        cpregnancy_type=request.POST.get('pregnancy_type')
        cpregnancy_date=request.POST.get('pregnancy_date')
        ccattle_id=request.POST.get('cattle_id')
        cpregnancy_status = request.POST.get('pregnancy_status')

        errors = []
        if cpregnancy_date:
            parsed_pregnancy_date = parse_date(cpregnancy_date)
            if not parsed_pregnancy_date:
                errors.append('Pregnancy date must be in YYYY-MM-DD format.')
            else:
                cpregnancy_date = parsed_pregnancy_date
        else:
            errors.append('Pregnancy date is required.')

        if not cpregnancy_type:
            errors.append('Pregnancy type is required.')

        if errors:
            context = {
                'errors': errors,
                "d": d, 
                "cattle": edit, 
                "cattles": Cattle.objects.all(),
            }
            return render(request, 'cattle/cattle_pregnancy_edit.html', context)
        
        edit.cattle_pregnancy_type = cpregnancy_type
        edit.cattle_pregnancy_date = cpregnancy_date
        edit.cattle_id = ccattle_id
        edit.pregnancy_status_id = cpregnancy_status
        
        edit.save()
        messages.warning(request, "Cattle Pregnancy Updated Successfully!")
        return redirect("/cattle_pregnancy")
    

    d = CattlePregnancy.objects.get(cattle_pregnancy_id=cattle_pregnancy_id)
    cattles = Cattle.objects.filter(cattle_gender="Female")
    statuses = PregnancyStatus.objects.all()
    context = {"d": d, "pregnancy": edit, "cattles": cattles, "statuses": statuses,}

    return render(request, 'cattle/cattle_pregnancy_edit.html', context)

def cattle_pregnancy_delete(request, cattle_pregnancy_id):
    if not request.user.has_perm('erp.delete_cattlepregnancy'):
        return HttpResponse('You are not authorised to view this page', status=403)
    d = CattlePregnancy.objects.get(cattle_pregnancy_id=cattle_pregnancy_id)
    d.delete()
    messages.error(request, "Cattle Pregnancy Deleted Successfully!")
    return redirect("/cattle_pregnancy")

@login_required(login_url='login')
def vaccine(request):
    if not request.user.has_perm('erp.view_vaccine'):
        return HttpResponse('You are not authorised to view this page', status=403)
    data = Vaccine.objects.all()
    paginated_data = paginate_data(request, data, 10) 
    context = {"data1":paginated_data}

    return render(request, 'cattle/vaccine.html', context)

@login_required(login_url='login')
def vaccine_add(request):
    if not request.user.has_perm('erp.add_vaccine'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method=="POST":
        cvaccine_name=request.POST.get('vaccine_name')
        cvaccine_benefit=request.POST.get('vaccine_benefit')
        cvaccine_recommended_time=request.POST.get('vaccine_recommended_time')

        query = Vaccine(vaccine_name=cvaccine_name, vaccine_benefit=cvaccine_benefit, vaccine_recommended_time=cvaccine_recommended_time)
        query.save()
        messages.success(request, "Vaccine Added Successfully!")
        return redirect("/vaccine")

    return render(request, 'cattle/vaccine_add.html')

@login_required(login_url='login')
def vaccine_edit(request,vaccine_id):
    if not request.user.has_perm('erp.change_vaccine'):
        return HttpResponse('You are not authorised to view this page', status=403)
    edit = Vaccine.objects.get(vaccine_id=vaccine_id)
    
    if request.method == "POST":
        cvaccine_name=request.POST.get('vaccine_name')
        cvaccine_benefit=request.POST.get('vaccine_benefit')
        cvaccine_recommended_time=request.POST.get('vaccine_recommended_time')

        edit.vaccine_name = cvaccine_name
        edit.vaccine_benefit = cvaccine_benefit
        edit.vaccine_recommended_time = cvaccine_recommended_time
        
        edit.save()
        messages.warning(request, "Vaccine Updated Successfully!")
        return redirect("/vaccine")

    d = Vaccine.objects.get(vaccine_id=vaccine_id)
    context = {"d": d}

    return render(request, 'cattle/vaccine_edit.html', context)

def vaccine_delete(request, vaccine_id):
    if not request.user.has_perm('erp.delete_vaccine'):
        return HttpResponse('You are not authorised to view this page', status=403)
    d = Vaccine.objects.get(vaccine_id=vaccine_id)
    d.delete()
    messages.error(request, "Vaccine Deleted Successfully!")
    return redirect("/vaccine")

@login_required(login_url='login')
def cattle_has_vaccine(request):
    if not request.user.has_perm('erp.view_cattlehasvaccine'):
        return HttpResponse('You are not authorised to view this page', status=403)
    data = CattleHasVaccine.objects.all()
    cattle = Cattle.objects.all()
    vaccine = Vaccine.objects.all()

    paginated_data = paginate_data(request, data, 10) 
    context = {"data1":paginated_data, 'cattle': cattle, 'vaccine': vaccine,}

    return render(request, 'cattle/cattle_has_vaccine.html', context)

@login_required(login_url='login')
def cattle_has_vaccine_add(request):
    if not request.user.has_perm('erp.add_cattlehasvaccine'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method=="POST":
        cvaccine_name=request.POST.get('vaccine_name')
        cgiven_time=request.POST.get('given_time')
        ccattle_id=request.POST.get('cattle_id')

        errors = []
        if cgiven_time:
            try:
                cgiven_time = datetime.strptime(cgiven_time, '%Y-%m-%dT%H:%M')
            except ValueError:
                errors.append('Invalid Given Time format. Use YYYY-MM-DDTHH:MM format.')
        else:
            cgiven_time = None 

        if errors:
            context = {
                'errors': errors,
                'data1': Cattle.objects.all(),
                'data2': Vaccine.objects.all()
            }
            return render(request, 'cattle/cattle_add.html', context)

        query = CattleHasVaccine(vaccine_id=cvaccine_name, cattle_given_time=cgiven_time, cattle_id=ccattle_id)
        query.save()
        messages.success(request, "Cattle Vaccination Added Successfully!")
        return redirect("/cattle_has_vaccine")
    
    cattle_data = Cattle.objects.all()
    vaccine_data = Vaccine.objects.all()
    context = {
        'data1': cattle_data,
        'data2': vaccine_data,
    }

    return render(request, 'cattle/cattle_has_vaccine_add.html', context)

@login_required(login_url='login')
def cattle_has_vaccine_edit(request,id):
    if not request.user.has_perm('erp.change_cattlehasvaccine'):
        return HttpResponse('You are not authorised to view this page', status=403)
    edit = CattleHasVaccine.objects.get(id=id)
    
    if request.method == "POST":
        cvaccine_name=request.POST.get('vaccine_name')
        cgiven_time=request.POST.get('given_time')
        ccattle_id=request.POST.get('cattle_id')

        errors = []
        if cgiven_time:
            try:
                cgiven_time = datetime.strptime(cgiven_time, '%Y-%m-%dT%H:%M')
            except ValueError:
                errors.append('Invalid Given Time format. Use YYYY-MM-DDTHH:MM format.')
        else:
            cgiven_time = None 

        if errors:
            context = {
                'errors': errors,
                'cattles': Cattle.objects.all(),
                'vaccines': Vaccine.objects.all(),
                "d": CattleHasVaccine.objects.get(id=id), 
                "cattle": edit, 
            }
            return render(request, 'cattle/cattle_add.html', context)

        edit.vaccine_id = cvaccine_name
        edit.cattle_given_time = cgiven_time
        edit.cattle_id = ccattle_id
        
        edit.save()
        messages.warning(request, "Cattle Vaccination Updated Successfully!")
        return redirect("/cattle_has_vaccine")
    

    d = CattleHasVaccine.objects.get(id=id)
    cattles = Cattle.objects.all()
    vaccines = Vaccine.objects.all()
    context = {"d": d, "cattle": edit, "cattles": cattles, "vaccines": vaccines,}

    return render(request, 'cattle/cattle_has_vaccine_edit.html', context)


def cattle_has_vaccine_delete(request, id):
    if not request.user.has_perm('erp.delete_cattlehasvaccine'):
        return HttpResponse('You are not authorised to view this page', status=403)
    d = CattleHasVaccine.objects.get(id=id)
    d.delete()
    messages.error(request, "Cattle Vaccination Deleted Successfully!")
    return redirect("/cattle_has_vaccine")

@login_required(login_url='login')
def medicine(request):
    if not request.user.has_perm('erp.view_medicine'):
        return HttpResponse('You are not authorised to view this page', status=403)
    data = Medicine.objects.all()
    paginated_data = paginate_data(request, data, 10) 
    context = {"data1":paginated_data}

    return render(request, 'cattle/medicine.html', context)

@login_required(login_url='login')
def medicine_add(request):
    if not request.user.has_perm('erp.add_medicine'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method=="POST":
        cname=request.POST.get('name')
        cbenefit=request.POST.get('benefit')
        cdate = datetime.now().date()

        query = Medicine(name=cname, benefit=cbenefit, modified_date=cdate)
        query.save()
        messages.success(request, "Medicine Added Successfully!")
        return redirect("/medicine")

    return render(request, 'cattle/medicine_add.html')

@login_required(login_url='login')
def medicine_edit(request, id):
    if not request.user.has_perm('erp.change_medicine'):
        return HttpResponse('You are not authorised to view this page', status=403)
    edit = Medicine.objects.get(id=id)
    
    if request.method == "POST":
        cname=request.POST.get('name')
        cbenefit=request.POST.get('benefit')
        cdate = datetime.now().date()

        edit.name = cname
        edit.benefit = cbenefit
        edit.modified_date=cdate
        
        edit.save()
        messages.warning(request, "Medicine Updated Successfully!")
        return redirect("/medicine")

    d = Medicine.objects.get(id=id)
    context = {"d": d}

    return render(request, 'cattle/medicine_edit.html', context)

def medicine_delete(request, id):
    if not request.user.has_perm('erp.delete_medicine'):
        return HttpResponse('You are not authorised to view this page', status=403)
    d = Medicine.objects.get(id=id)
    d.delete()
    messages.error(request, "Medicine Deleted Successfully!")
    return redirect("/medicine")  

@login_required(login_url='login')
def cattle_health_checkup(request):
    if not request.user.has_perm('erp.view_cattlehealthcheckup'):
        return HttpResponse('You are not authorised to view this page', status=403)
    data = CattleHealthCheckup.objects.all()
    cattle = Cattle.objects.all()
    person = Person.objects.all()
    employee = Employee.objects.all()

    paginated_data = paginate_data(request, data, 10) 

    context = {"data1":paginated_data, 'cattle': cattle, 'person': person, 'employee': employee,}

    return render(request, 'cattle/cattle_health_checkup.html', context)

@login_required(login_url='login')
def cattle_health_checkup_view(request, id):
    if not request.user.has_perm('erp.view_cattlehealthcheckup'):
        return HttpResponse('You are not authorised to view this page', status=403)
    health = get_object_or_404(CattleHealthCheckup, id=id)
    symptom_data = HealthCheckupSymptoms.objects.filter(cattle_health_checkup_id=id)
    medicine_data = CattleHealthCheckupHasMedicine.objects.filter(cattle_health_checkup_id=id)

    context = {"health":health, "medicine_data":medicine_data, "symptom_data":symptom_data}

    return render(request, 'cattle/cattle_health_checkup_view.html', context)

@login_required(login_url='login')
def cattle_health_checkup_add(request):
    if not request.user.has_perm('erp.add_cattlehealthcheckup'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method=="POST":
        ccattle_id=request.POST.get('cattle_id')
        cfindings=request.POST.get('findings')
        cchecked_by=request.POST.get('checked_by')


        query = CattleHealthCheckup(findings=cfindings, checked_by_id=cchecked_by, cattle_id=ccattle_id,)
        query.save()
        messages.success(request, "Cattle Checkup Added Successfully!")
        return redirect("/cattle_health_checkup")
    
    cattle_data = Cattle.objects.all()
    person_data = Person.objects.all()
    context = {
        'data1': cattle_data,
        'data2': person_data,
    }

    return render(request, 'cattle/cattle_health_checkup_add.html', context)

@login_required(login_url='login')
def cattle_health_checkup_edit(request, id):
    if not request.user.has_perm('erp.change_cattlehealthcheckup'):
        return HttpResponse('You are not authorised to view this page', status=403)
    edit = CattleHealthCheckup.objects.get(id=id)
    
    if request.method == "POST":
        ccattle_id=request.POST.get('cattle_id')
        cfindings=request.POST.get('findings')
        cchecked_by=request.POST.get('checked_by')

        edit.cattle_id = ccattle_id
        edit.findings = cfindings
        edit.checked_by_id=cchecked_by
        
        edit.save()
        messages.warning(request, "Checkup Updated Successfully!")
        return redirect("/cattle_health_checkup")

    d = CattleHealthCheckup.objects.get(id=id)
    cattles = Cattle.objects.all()
    persons = Person.objects.all()
    context = {"d": d, "cattle": edit, "cattles": cattles, "persons": persons,}

    return render(request, 'cattle/cattle_health_checkup_edit.html', context)

def cattle_health_checkup_delete(request, id):
    if not request.user.has_perm('erp.delete_cattlehealthcheckup'):
        return HttpResponse('You are not authorised to view this page', status=403)
    d = CattleHealthCheckup.objects.get(id=id)
    d.delete()
    messages.error(request, "Checkup Deleted Successfully!")
    return redirect("/cattle_health_checkup") 

@login_required(login_url='login')
def checkup_medicine_add(request, id):
    if not request.user.has_perm('erp.add_cattlehealthcheckuphasmedicine'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method == "POST":
        checkup_id = request.POST.get('checkup_id')
        instruction = request.POST.get('instruction')
        medicine_id = request.POST.get('medicine_id')
        modified_date = datetime.now()

        query = CattleHealthCheckupHasMedicine(
            cattle_health_checkup_id=checkup_id,
            giving_instruction=instruction,
            medicine_id=medicine_id,
            modified_date=modified_date,
        )
        query.save()
        messages.success(request, "Cattle Medicine Added Successfully!")
        return redirect(f"/cattle_health_checkup_view/{id}")
    
    checkup_data = CattleHealthCheckup.objects.all()
    medicine_data = Medicine.objects.all()

    context = {
        'data1': checkup_data,
        'data2': medicine_data,
        'current_checkup_id': id,
    }

    return render(request, 'cattle/checkup_medicine_add.html', context)

@login_required(login_url='login')
def checkup_medicine_edit(request, id):
    if not request.user.has_perm('erp.change_cattlehealthcheckuphasmedicine'):
        return HttpResponse('You are not authorised to view this page', status=403)
    edit = get_object_or_404(CattleHealthCheckupHasMedicine, id=id)
    
    if request.method == "POST":
        checkup_id = request.POST.get('checkup_id')
        instruction = request.POST.get('instruction')
        medicine_id = request.POST.get('medicine_id')
        modified_date = datetime.now()
        
        edit.cattle_health_checkup_id = checkup_id
        edit.giving_instruction = instruction
        edit.medicine_id = medicine_id
        edit.modified_date = modified_date
        
        edit.save()
        messages.warning(request, "Medicine Updated Successfully!")
        return redirect('/cattle_health_checkup')

    d = CattleHealthCheckupHasMedicine.objects.get(id=id)
    medicine_data = Medicine.objects.all()
    
    context = {
        'data2' : medicine_data,
        'd': d,
    }

    return render(request, 'cattle/checkup_medicine_edit.html', context)

def checkup_medicine_delete(request, id):
    if not request.user.has_perm('erp.delete_cattlehealthcheckuphasmedicine'):
        return HttpResponse('You are not authorised to view this page', status=403)
    d = CattleHealthCheckupHasMedicine.objects.get(id=id)
    id = d.id
    d.delete()
    messages.error(request, "Medicine Deleted Successfully!")
    return redirect('/cattle_health_checkup')


@login_required(login_url='login')
def checkup_symptom_add(request, id):
    if not request.user.has_perm('erp.add_healthcheckupsymptoms'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method == "POST":
        checkup_id = request.POST.get('checkup_id')
        symptom = request.POST.get('symptom')
        modified_date = datetime.now()
        checkup_id = request.POST.get('checkup_id')

        query = HealthCheckupSymptoms(
            cattle_health_checkup_id=checkup_id,
            symptom=symptom,
            modified_date=modified_date,
        )
        query.save()
        messages.success(request, "Cattle Symptom Added Successfully!")
        return redirect(f"/cattle_health_checkup_view/{id}")
    
    checkup_data = CattleHealthCheckup.objects.all()

    context = {
        'data1': checkup_data,
        'current_checkup_id': id,
    }

    return render(request, 'cattle/checkup_symptom_add.html', context)

@login_required(login_url='login')
def checkup_symptom_edit(request, id):
    if not request.user.has_perm('erp.change_healthcheckupsymptoms'):
        return HttpResponse('You are not authorised to view this page', status=403)
    edit = get_object_or_404(HealthCheckupSymptoms, id=id)
    
    if request.method == "POST":
        checkup_id = request.POST.get('checkup_id')
        symptom = request.POST.get('symptom')
        modified_date = datetime.now()
        
        edit.cattle_health_checkup_id = checkup_id
        edit.symptom = symptom
        edit.modified_date = modified_date
        
        edit.save()
        messages.warning(request, "Symptom Updated Successfully!")
        return redirect('/cattle_health_checkup')

    d = HealthCheckupSymptoms.objects.get(id=id)
    
    context = {
        'd': d,
    }

    return render(request, 'cattle/checkup_symptom_edit.html', context)

def checkup_symptom_delete(request, id):
    if not request.user.has_perm('erp.delete_healthcheckupsymptoms'):
        return HttpResponse('You are not authorised to view this page', status=403)
    d = HealthCheckupSymptoms.objects.get(id=id)
    id = d.id
    d.delete()
    messages.error(request, "Symptom Deleted Successfully!")
    return redirect('/cattle_health_checkup')


@login_required(login_url='login')
def milk_production(request):
    if not request.user.has_perm('erp.view_milkproduction'):
        return HttpResponse('You are not authorised to view this page', status=403)
    data = MilkProduction.objects.all()
    cattle = Cattle.objects.all()

    paginated_data = paginate_data(request, data, 10) 

    context = {"data1":paginated_data, 'cattle': cattle,}

    return render(request, 'cattle/milk_production.html', context)

@login_required(login_url='login')
def milk_production_add(request):
    if not request.user.has_perm('erp.add_milkproduction'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method=="POST":
        camount_in_liter=request.POST.get('amount_in_liter')
        cmilk_time=request.POST.get('milk_time')
        cfat_content=request.POST.get('fat_content')
        cprotein_content=request.POST.get('protein_content')
        csomatic_cell_count=request.POST.get('somatic_cell_count')
        cduration_in_min=request.POST.get('duration_in_min')
        ccattle_id=request.POST.get('cattle_id')

        errors = []
 
        if cmilk_time:
            try:
                cmilk_time = datetime.strptime(cmilk_time, '%Y-%m-%dT%H:%M')
            except ValueError:
                errors.append('Invalid Milk Time format. Use YYYY-MM-DDTHH:MM format.')
        else:
            cmilk_time = None 

        if camount_in_liter:
            try:
                camount_in_liter = float(camount_in_liter)
                if camount_in_liter <= 0:
                    errors.append("Amount in Liter must be a positive number.")
            except ValueError:
                errors.append("Amount in liter must be a number.")
        else:
            camount_in_liter = None

        if cfat_content:
            try:
                cfat_content = float(cfat_content)
            except ValueError:
                errors.append('Fat content must be a number.')
        else:
            cfat_content = 0 

        if cprotein_content:
            try:
                cprotein_content = float(cprotein_content)
            except ValueError:
                errors.append('Protein content must be a number.')
        else:
            cprotein_content = 0 

        if csomatic_cell_count:
            try:
                csomatic_cell_count = float(csomatic_cell_count)
            except ValueError:
                errors.append('Somatic cell count content must be a number.')
        else:
            csomatic_cell_count = 0 

        if cduration_in_min:
            try:
                cduration_in_min = float(cduration_in_min)
                if cduration_in_min < 0:
                    errors.append("Duration in min count must be a positive number.")
            except ValueError:
                errors.append('Duration in min count must be a number.')
        else:
            cduration_in_min = 0 
            
        if errors:
            context = {
                'errors': errors,
                'data2': Cattle.objects.all(),
            }
            return render(request, 'cattle/milk_production_add.html', context)

        query = MilkProduction(amount_in_liter=camount_in_liter, milk_time=cmilk_time, fat_content=cfat_content, protein_content=cprotein_content, somatic_cell_count=csomatic_cell_count, duration_in_min=cduration_in_min, cattle_id=ccattle_id)
        query.save()
        messages.success(request, "Milk Production Added Successfully!")
        return redirect("/milk_production")
    
    cattle_data = Cattle.objects.all()
    context = {
        'data2': cattle_data,
    }

    return render(request, 'cattle/milk_production_add.html',context)

@login_required(login_url='login')
def milk_production_edit(request,milk_production_id):
    if not request.user.has_perm('erp.change_milkproduction'):
        return HttpResponse('You are not authorised to view this page', status=403)

    edit = MilkProduction.objects.get(milk_production_id=milk_production_id)
    
    if request.method == "POST":
        camount_in_liter=request.POST.get('amount_in_liter')
        cmilk_time=request.POST.get('milk_time')
        cfat_content=request.POST.get('fat_content')
        cprotein_content=request.POST.get('protein_content')
        csomatic_cell_count=request.POST.get('somatic_cell_count')
        cduration_in_min=request.POST.get('duration_in_min')
        ccattle_id=request.POST.get('cattle_id')

        errors = []

        if cmilk_time:
            try:
                cmilk_time = datetime.strptime(cmilk_time, '%Y-%m-%dT%H:%M')
            except ValueError:
                errors.append('Invalid Milk Time format. Use YYYY-MM-DDTHH:MM format.')
        else:
            cmilk_time = None 
            
        if camount_in_liter:
            try:
                camount_in_liter = float(camount_in_liter)
                if camount_in_liter <= 0:
                    errors.append("Amount in Liter must be a positive number.")
            except ValueError:
                errors.append("Amount in liter must be a number.")
        else:
            camount_in_liter = None

        if cfat_content:
            try:
                cfat_content = float(cfat_content)
            except ValueError:
                errors.append('Fat content must be a number.')
        else:
            cfat_content = 0 

        if cprotein_content:
            try:
                cprotein_content = float(cprotein_content)
            except ValueError:
                errors.append('Protein content must be a number.')
        else:
            cprotein_content = 0 

        if csomatic_cell_count:
            try:
                csomatic_cell_count = float(csomatic_cell_count)
            except ValueError:
                errors.append('Somatic cell count content must be a number.')
        else:
            csomatic_cell_count = 0 

        if cduration_in_min:
            try:
                cduration_in_min = float(cduration_in_min)
                if cduration_in_min < 0:
                    errors.append("Duration in min count must be a positive number.")
            except ValueError:
                errors.append('Duration in min count must be a number.')
        else:
            cduration_in_min = 0 
            
        if errors:
            context = {
                'cattle': edit,
                'errors': errors,
                'cattles': Cattle.objects.all(),
                'd': MilkProduction.objects.get(milk_production_id=milk_production_id)

            }
            return render(request, 'cattle/milk_production_edit.html', context)
        
        edit.amount_in_liter = camount_in_liter
        edit.milk_time = cmilk_time
        edit.fat_content = cfat_content
        edit.protein_content = cprotein_content
        edit.somatic_cell_count = csomatic_cell_count
        edit.duration_in_min = cduration_in_min
        edit.cattle_id = ccattle_id
        
        edit.save()
        messages.warning(request, "Milk Production Updated Successfully!")
        return redirect("/milk_production")

    d = MilkProduction.objects.get(milk_production_id=milk_production_id)
    cattles = Cattle.objects.all()
    context = {"d": d, "cattle": edit, "cattles": cattles}

    return render(request, 'cattle/milk_production_edit.html', context)

def milk_production_delete(request, milk_production_id):
    if not request.user.has_perm('erp.delete_milkproduction'):
        return HttpResponse('You are not authorised to view this page', status=403)
    d = MilkProduction.objects.get(milk_production_id=milk_production_id)
    d.delete()
    messages.error(request, "Milk Production Deleted Successfully!")
    return redirect("/milk_production")

@login_required(login_url='login')
def feed_formulation(request):
    if not request.user.has_perm('erp.view_feedformulation'):
        return HttpResponse('You are not authorised to view this page', status=403)
    data = FeedFormulation.objects.all()
    paginated_data = paginate_data(request, data, 10) 
    context = {"data1":paginated_data}

    return render(request, 'feed/feed_formulation.html', context)

@login_required(login_url='login')
def feed_formulation_view(request, id):
    if not request.user.has_perm('erp.view_feedformulation'):
        return HttpResponse('You are not authorised to view this page', status=403)
    feed = get_object_or_404(FeedFormulation, id=id)
    ingredient_data = FeedIngredient.objects.filter(feed_formulation_id=id)

    item_data = Item.objects.all()
    measurement_data = ItemMeasurement.objects.all()

    context = {"feed":feed, "ingredient_data":ingredient_data, "item_data":item_data, "measurement_data":measurement_data,}

    return render(request, 'feed/feed_formulation_view.html', context)

@login_required(login_url='login')
def feed_formulation_add(request):
    if not request.user.has_perm('erp.add_feedformulation'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method=="POST":
        cname=request.POST.get('name')
        cstart_age_in_weeks=request.POST.get('start_age_in_weeks')
        cend_age_in_weeks=request.POST.get('end_age_in_weeks')
        cmodified_date=datetime.now().date()

        query = FeedFormulation(name=cname, start_age_in_weeks=cstart_age_in_weeks, end_age_in_weeks=cend_age_in_weeks, modified_date= cmodified_date)
        query.save()
        messages.success(request, "Feed Formulation Added Successfully!")
        return redirect("/feed_formulation")

    return render(request, 'feed/feed_formulation_add.html')

@login_required(login_url='login')
def feed_formulation_edit(request,id):
    if not request.user.has_perm('erp.change_feedformulation'):
        return HttpResponse('You are not authorised to view this page', status=403)
    edit = FeedFormulation.objects.get(id=id)
    
    if request.method == "POST":
        cname=request.POST.get('name')
        cstart_age_in_weeks=request.POST.get('start_age_in_weeks')
        cend_age_in_weeks=request.POST.get('end_age_in_weeks')
        cmodified_date=datetime.now().date()
        
        edit.name = cname
        edit.start_age_in_weeks = cstart_age_in_weeks
        edit.end_age_in_weeks = cend_age_in_weeks
        edit.modified_date = cmodified_date
        
        edit.save()
        messages.warning(request, "Feed Formulation Updated Successfully!")
        return redirect("/feed_formulation")

    d = FeedFormulation.objects.get(id=id)
    context = {"d": d}

    return render(request, 'feed/feed_formulation_edit.html', context)

def feed_formulation_delete(request, id):
    if not request.user.has_perm('erp.delete_feedformulation'):
        return HttpResponse('You are not authorised to view this page', status=403)
    d = FeedFormulation.objects.get(id=id)
    d.delete()
    messages.error(request, "Feed Formulation Deleted Successfully!")
    return redirect("/feed_formulation")

@login_required(login_url='login')
def ingredient_add(request, id):
    if not request.user.has_perm('erp.add_feedingredient'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method=="POST":
        cfeed_formulation_id=request.POST.get('feed_formulation_id')
        citem_id=request.POST.get('item_id')
        citem_measurement_id=request.POST.get('item_measurement_id')
        cquantity=request.POST.get('quantity')
        cmodified_date=datetime.now().date()

        errors = []
        if cquantity:
            try:
                cquantity = float(cquantity)
                if cquantity <= 0:
                    errors.append("Quantity must be a positive number.")
            except ValueError:
                errors.append("Quantity must be a valid number.")
        else:
            cquantity = None

        if errors:
            context = {
                'errors': errors,
                'data1': Item.objects.all(),
                'data2': ItemMeasurement.objects.all(),
                'data3': FeedFormulation.objects.all(),
            }
 
            return render(request, 'feed/ingredient_add.html', context)

        query = FeedIngredient(feed_formulation_id=cfeed_formulation_id, item_id=citem_id, item_measurement_id=citem_measurement_id, quantity=cquantity, modified_date=cmodified_date)
        query.save()
        messages.success(request, "Feed Ingredient Added Successfully!")
        return redirect(f"/feed_formulation_view/{id}")
    
    item_data = Item.objects.all()
    measurement_data = ItemMeasurement.objects.all()
    formulation_data = FeedFormulation.objects.all()

    ingredient_data = FeedIngredient.objects.all()

    context = {"data1":item_data, 'data2': measurement_data, 'data3': formulation_data,'current_formulation_id': id, 'ingredient_data':ingredient_data}

    return render(request, 'feed/ingredient_add.html', context)

@login_required(login_url='login')
def ingredient_edit(request,id):
    if not request.user.has_perm('erp.change_feedingredient'):
        return HttpResponse('You are not authorised to view this page', status=403)
    edit = FeedIngredient.objects.get(id=id)
    
    if request.method == "POST":
        cfeed_formulation_id=request.POST.get('feed_formulation_id')
        citem_id=request.POST.get('item_id')
        citem_measurement_id=request.POST.get('item_measurement_id')
        cquantity=request.POST.get('quantity')
        cmodified_date=datetime.now().date()

        errors = []
        if cquantity:
            try:
                cquantity = float(cquantity)
                if cquantity <= 0:
                    errors.append("Quantity must be a positive number.")
            except ValueError:
                errors.append("Quantity must be a valid number.")
        else:
            cquantity = None

        if errors:
            context = {
                'errors': errors,
                "d": FeedIngredient.objects.get(id=id),
                "item": edit,
                'data1': Item.objects.all(),
                'data2': ItemMeasurement.objects.all(),
                'data3': ItemType.objects.all(),
            }
 
            return render(request, 'feed/ingredient_edit.html', context)
        
        edit.feed_formulation_id = cfeed_formulation_id
        edit.item_id = citem_id
        edit.item_measurement_id = citem_measurement_id
        edit.quantity = cquantity
        edit.modified_date = cmodified_date
        
        edit.save()
        messages.warning(request, "Feed Ingredient Updated Successfully!")
        return redirect("/feed_formulation")

    d = FeedIngredient.objects.get(id=id)
    item_data = Item.objects.all()
    measurement_data = ItemMeasurement.objects.all()
    formulation_data = FeedFormulation.objects.all()
    context = {"d": d,"item": edit, "data1":item_data, 'data2': measurement_data, 'data3': formulation_data,}

    return render(request, 'feed/ingredient_edit.html', context)

def ingredient_delete(request, id):
    if not request.user.has_perm('erp.delete_feedingredient'):
        return HttpResponse('You are not authorised to view this page', status=403)
    d = FeedIngredient.objects.get(id=id)
    d.delete()
    messages.error(request, "Feed Ingredient Deleted Successfully!")
    return redirect("/feed_formulation")


@login_required(login_url='login')
def cattle_has_feed(request):
    if not request.user.has_perm('erp.view_cattlehasfeed'):
        return HttpResponse('You are not authorised to view this page', status=403)
    data = CattleHasFeed.objects.all()
    paginated_data = paginate_data(request, data, 10) 

    cattle_data = Cattle.objects.all()
    shift_data = Shift.objects.all()
    formulation_data = FeedFormulation.objects.all()
    context = {"data1":paginated_data, "cattle_data":cattle_data, "shift_data":shift_data, "formulation_data":formulation_data,}

    return render(request, 'feed/cattle_has_feed.html', context)

@login_required(login_url='login')
def cattle_has_feed_add(request):
    if not request.user.has_perm('erp.add_cattlehasfeed'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method=="POST":
        ccattle_farm_entity_id=request.POST.get('cattle_farm_entity_id')
        cfeed_formulation_id=request.POST.get('feed_formulation_id')
        cshift_id=request.POST.get('shift_id')
        cfeed_time=request.POST.get('feed_time')
        cconsumption_status=request.POST.get('consumption_status')
        cmodified_date=datetime.now().date()

        errors = []
        if cfeed_time:
            try:
                cfeed_time = datetime.strptime(cfeed_time, '%Y-%m-%dT%H:%M')
            except ValueError:
                errors.append('Invalid Feed Time format. Use YYYY-MM-DDTHH:MM format.')
        else:
            cfeed_time = None 

        if errors:
            context = {
                'errors': errors,
                'data1': Cattle.objects.all(),
                'data2': Shift.objects.all(),
                'data3': FeedFormulation.objects.all(),
            }
 
            return render(request, 'feed/cattle_has_feed_add.html', context)

        query = CattleHasFeed(cattle_farm_entity_id=ccattle_farm_entity_id, feed_formulation_id=cfeed_formulation_id, shift_id=cshift_id, feed_time=cfeed_time,consumption_status=cconsumption_status, modified_date=cmodified_date)
        query.save()
        messages.success(request, "Cattle Feed Added Successfully!")
        return redirect("/cattle_has_feed")
    
    cattle_data = Cattle.objects.all()
    shift_data = Shift.objects.all()
    formulation_data = FeedFormulation.objects.all()

    context = {"data1":cattle_data, 'data2': shift_data, 'data3': formulation_data,}

    return render(request, 'feed/cattle_has_feed_add.html', context)

@login_required(login_url='login')
def cattle_has_feed_edit(request,id):
    if not request.user.has_perm('erp.change_cattlehasfeed'):
        return HttpResponse('You are not authorised to view this page', status=403)
    edit = CattleHasFeed.objects.get(id=id)
    
    if request.method == "POST":
        ccattle_farm_entity_id=request.POST.get('cattle_farm_entity_id')
        cfeed_formulation_id=request.POST.get('feed_formulation_id')
        cshift_id=request.POST.get('shift_id')
        cfeed_time=request.POST.get('feed_time')
        cconsumption_status=request.POST.get('consumption_status')
        cmodified_date=datetime.now().date()

        errors = []
        if cfeed_time:
            try:
                cfeed_time = datetime.strptime(cfeed_time, '%Y-%m-%dT%H:%M')
            except ValueError:
                errors.append('Invalid Feed Time format. Use YYYY-MM-DDTHH:MM format.')
        else:
            cfeed_time = None 

        if errors:
            context = {
                'errors': errors,
                "d": CattleHasFeed.objects.get(id=id),
                "item": edit,
                'data1': Cattle.objects.all(),
                'data2': Shift.objects.all(),
                'data3': FeedFormulation.objects.all(),
            }

            return render(request, 'feed/cattle_has_feed_edit.html', context)
        
        edit.cattle_farm_entity_id = ccattle_farm_entity_id
        edit.feed_formulation_id = cfeed_formulation_id
        edit.shift_id = cshift_id
        edit.feed_time = cfeed_time
        edit.consumption_status = cconsumption_status
        edit.modified_date = cmodified_date
        
        edit.save()
        messages.warning(request, "Cattle Feed Updated Successfully!")
        return redirect("/cattle_has_feed")

    d = CattleHasFeed.objects.get(id=id)
    cattle_data = Cattle.objects.all()
    shift_data = Shift.objects.all()
    formulation_data = FeedFormulation.objects.all()
    context = {"d": d,"item": edit, "data1":cattle_data, 'data2': shift_data, 'data3': formulation_data,}

    return render(request, 'feed/cattle_has_feed_edit.html', context)

def cattle_has_feed_delete(request, id):
    if not request.user.has_perm('erp.delete_cattlehasfeed'):
        return HttpResponse('You are not authorised to view this page', status=403)
    d = CattleHasFeed.objects.get(id=id)
    d.delete()
    messages.error(request, "Cattle Feed Deleted Successfully!")
    return redirect("/cattle_has_feed")



@login_required(login_url='login')
def person_type(request):
    if not request.user.has_perm('erp.view_persontype'):
        return HttpResponse('You are not authorised to view this page', status=403)
    data = PersonType.objects.all()
    paginated_data = paginate_data(request, data, 10) 
    context = {"data1":paginated_data}

    return render(request, 'person/person_type.html', context)

@login_required(login_url='login')
def person_type_add(request):
    if not request.user.has_perm('erp.add_persontype'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method=="POST":
        cperson_type=request.POST.get('person_type')
        cdate = datetime.now().date()

        query = PersonType(person_type=cperson_type, modified_date=cdate)
        query.save()
        messages.success(request, "Person Type Added Successfully!")
        return redirect("/person_type")

    return render(request, 'person/person_type_add.html')

@login_required(login_url='login')
def person_type_edit(request,person_type_id):
    if not request.user.has_perm('erp.change_persontype'):
        return HttpResponse('You are not authorised to view this page', status=403)
    edit = PersonType.objects.get(person_type_id=person_type_id)
    
    if request.method == "POST":
        cperson_type=request.POST.get('person_type')
        cdate = datetime.now().date()
        
        edit.person_type = cperson_type
        edit.modified_date = cdate

        edit.save()
        messages.warning(request, "Person Type Updated Successfully!")
        return redirect("/person_type")

    d = PersonType.objects.get(person_type_id=person_type_id)
    context = {"d": d}

    return render(request, 'person/person_type_edit.html', context)

def person_type_delete(request, person_type_id):
    if not request.user.has_perm('erp.delete_persontype'):
        return HttpResponse('You are not authorised to view this page', status=403)
    d = PersonType.objects.get(person_type_id=person_type_id)
    d.delete()
    messages.error(request, "Person Type Deleted Successfully!")
    return redirect("/person_type")

@login_required(login_url='login')
def person_title(request):
    if not request.user.has_perm('erp.view_persontitle'):
        return HttpResponse('You are not authorised to view this page', status=403)
    data = PersonTitle.objects.all()
    paginated_data = paginate_data(request, data, 10) 
    context = {"data1":paginated_data}

    return render(request, 'person/person_title.html', context)

@login_required(login_url='login')
def person_title_add(request):
    if not request.user.has_perm('erp.add_persontitle'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method=="POST":
        cperson_title=request.POST.get('person_title')
        cdate = datetime.now().date()

        query = PersonTitle(person_title=cperson_title, modified_date=cdate)
        query.save()
        messages.success(request, "Person Title Added Successfully!")
        return redirect("/person_title")

    return render(request, 'person/person_title_add.html')

@login_required(login_url='login')
def person_title_edit(request,person_title_id):
    if not request.user.has_perm('erp.change_persontitle'):
        return HttpResponse('You are not authorised to view this page', status=403)
    edit = PersonTitle.objects.get(person_title_id=person_title_id)
    
    if request.method == "POST":
        cperson_title=request.POST.get('person_title')
        cdate = datetime.now().date()
        
        edit.person_title = cperson_title
        edit.modified_date = cdate
        
        edit.save()
        messages.warning(request, "Person Title Updated Successfully!")
        return redirect("/person_title")

    d = PersonTitle.objects.get(person_title_id=person_title_id)
    context = {"d": d}

    return render(request, 'person/person_title_edit.html', context)

def person_title_delete(request, person_title_id):
    if not request.user.has_perm('erp.delete_persontitle'):
        return HttpResponse('You are not authorised to view this page', status=403)
    d = PersonTitle.objects.get(person_title_id=person_title_id)
    d.delete()
    messages.error(request, "Person Title Deleted Successfully!")
    return redirect("/person_title")

@login_required(login_url='login')
def contact_type(request):
    if not request.user.has_perm('erp.view_contacttype'):
        return HttpResponse('You are not authorised to view this page', status=403)
    data = ContactType.objects.all()
    paginated_data = paginate_data(request, data, 10) 
    context = {"data1":paginated_data}

    return render(request, 'person/contact_type.html', context)

@login_required(login_url='login')
def contact_type_add(request):
    if not request.user.has_perm('erp.add_contacttype'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method=="POST":
        ccontact_type=request.POST.get('contact_type')
        ccontact_type_desc=request.POST.get('description')
        cdate = datetime.now().date()

        query = ContactType(contact_type=ccontact_type, contact_type_desc=ccontact_type_desc, modified_date=cdate)
        query.save()
        messages.success(request, "Contact Type Added Successfully!")
        return redirect("/contact_type")

    return render(request, 'person/contact_type_add.html')

@login_required(login_url='login')
def contact_type_edit(request,contact_id):
    if not request.user.has_perm('erp.change_contacttype'):
        return HttpResponse('You are not authorised to view this page', status=403)
    edit = ContactType.objects.get(contact_id=contact_id)
    
    if request.method == "POST":
        ccontact_type=request.POST.get('contact_type')
        ccontact_type_desc=request.POST.get('description')
        cdate = datetime.now().date()
        
        edit.contact_type = ccontact_type
        edit.contact_type_desc = ccontact_type_desc
        edit.modified_date = cdate
        
        edit.save()
        messages.warning(request, "Contact Type Updated Successfully!")
        return redirect("/contact_type")

    d = ContactType.objects.get(contact_id=contact_id)
    context = {"d": d}

    return render(request, 'person/contact_type_edit.html', context)

def contact_type_delete(request, contact_id):
    if not request.user.has_perm('erp.delete_contacttype'):
        return HttpResponse('You are not authorised to view this page', status=403)
    d = ContactType.objects.get(contact_id=contact_id)
    d.delete()
    messages.error(request, "Contact Type Deleted Successfully!")
    return redirect("/contact_type")


@login_required(login_url='login')
def payment_method(request):
    if not request.user.has_perm('erp.view_paymentmethod'):
        return HttpResponse('You are not authorised to view this page', status=403)
    data = PaymentMethod.objects.all()
    paginated_data = paginate_data(request, data, 10) 
    context = {"data1":paginated_data}

    return render(request, 'sales/payment_method.html', context)

@login_required(login_url='login')
def payment_method_add(request):
    if not request.user.has_perm('erp.add_paymentmethod'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method=="POST":
        cpayment_method=request.POST.get('payment_method')
        cdate = datetime.now().date()

        query = PaymentMethod(payment_method=cpayment_method, modified_date=cdate)
        query.save()
        messages.success(request, "Payment Method Added Successfully!")
        return redirect("/payment_method")

    return render(request, 'sales/payment_method_add.html')

@login_required(login_url='login')
def payment_method_edit(request,id):
    if not request.user.has_perm('erp.change_paymentmethod'):
        return HttpResponse('You are not authorised to view this page', status=403)
    edit = PaymentMethod.objects.get(id=id)
    
    if request.method == "POST":
        cpayment_method=request.POST.get('payment_method')
        cdate = datetime.now().date()
        
        edit.payment_method = cpayment_method
        edit.modified_date = cdate
        
        edit.save()
        messages.warning(request, "Payment Method Updated Successfully!")
        return redirect("/payment_method")

    d = PaymentMethod.objects.get(id=id)
    context = {"d": d}

    return render(request, 'sales/payment_method_edit.html', context)

def payment_method_delete(request, id):
    if not request.user.has_perm('erp.delete_paymentmethod'):
        return HttpResponse('You are not authorised to view this page', status=403)
    d = PaymentMethod.objects.get(id=id)
    d.delete()
    messages.error(request, "Payment Method Deleted Successfully!")
    return redirect("/payment_method")


@login_required(login_url='login')
def customer(request):
    if not request.user.has_perm('erp.view_customer'):
        return HttpResponse('You are not authorised to view this page', status=403)
    
    customers = Customer.objects.all()
    all_contacts = FarmEntityContact.objects.filter(
        contact_type__contact_type__in=['Phone_Safaricom', 'Phone_Ethiotel', 'Email']
    )
    
    customers_with_contacts = customers.prefetch_related(
        Prefetch('person_farm_entity__farm_entity__farmentitycontact_set', queryset=all_contacts, to_attr='contacts')
    )

    all_addresses = FarmEntityAddress.objects.all()
    address_dict = {address.farm_entity_id: address for address in all_addresses}
    
    customer_contact_info = []
    for customer in customers_with_contacts:
        phone_contact = None
        phone_contact2 = None
        email_contact = None
        
        for contact in customer.person_farm_entity.farm_entity.contacts:
            if contact.contact_type.contact_type == 'Phone_Safaricom' and not phone_contact:
                phone_contact = contact.contact
            if contact.contact_type.contact_type == 'Phone_Ethiotel' and not phone_contact2:
                phone_contact2 = contact.contact
            if contact.contact_type.contact_type == 'Email' and not email_contact:
                email_contact = contact.contact
        
        customer_contact_info.append({
            'customer': customer,
            'phone_contact': phone_contact,
            'phone_contact2': phone_contact2,
            'email_contact': email_contact,
            'address': address_dict.get(customer.person_farm_entity.farm_entity_id),
        })
    
    paginated_data = paginate_data(request, customer_contact_info, 10)

    context = {
        "data1": paginated_data,
    }

    return render(request, 'sales/customer.html', context)


@login_required(login_url='login')
def customer_add(request):
    if not request.user.has_perm('erp.add_customer'):
        return HttpResponse('You are not authorised to view this page', status=403)
    
    if request.method == "POST":
        cfirst_name = request.POST.get('first_name')
        cmiddle_name = request.POST.get('middle_name')
        cperson_type_id = "Customer"  

        try:
            farm_entity = FarmEntity.objects.create(modified_date=timezone.now())
            person_type = get_object_or_404(PersonType, person_type=cperson_type_id)
            
            person = Person.objects.create(
                farm_entity=farm_entity,
                first_name=cfirst_name,
                middle_name=cmiddle_name,
                person_type=person_type
            )
            
            Customer.objects.create(person_farm_entity_id=person.farm_entity.farm_entity_id)
            
            messages.success(request, "Customer Added Successfully!")
            return redirect("/customer")

        except Exception as e:
            messages.error(request, f"Error creating customer: {str(e)}")
            return redirect('/customer')
    
    person_types = PersonType.objects.all()
    context = {
        'data1': person_types,
    }

    return render(request, 'sales/customer_add.html', context)

@login_required(login_url='login')
def customer_edit(request, customer_id):
    if not request.user.has_perm('erp.change_customer'):
        return HttpResponse('You are not authorized to view this page', status=403)
    
    customer = get_object_or_404(Customer, customer_id=customer_id)
    person = customer.person_farm_entity
    
    if request.method == "POST":
        cfirst_name = request.POST.get('first_name')
        cmiddle_name = request.POST.get('middle_name')
        cperson_type_id = "Customer" 

        try:
            person_type = get_object_or_404(PersonType, person_type=cperson_type_id)

            person.first_name = cfirst_name
            person.middle_name = cmiddle_name
            person.person_type_id = person_type
            person.save()

            messages.warning(request, "Customer Updated Successfully!")
            return redirect("/customer")

        except Exception as e:
            messages.error(request, f"Error updating customer: {str(e)}")
            return redirect('/customer')

    data1 = PersonType.objects.all()
    data2 = ContactType.objects.all()
    data3 = Region.objects.all()
    context = {
        'data1': data1,
        'data2': data2,
        'data3': data3,
        'customer': customer,
        'person': person, 
    }

    return render(request, 'sales/customer_edit.html', context)

def customer_delete(request, customer_id):
    if not request.user.has_perm('erp.delete_customer'):
        return HttpResponse('You are not authorised to view this page', status=403)
    
    customer = get_object_or_404(Customer, customer_id=customer_id)
    person = customer.person_farm_entity 
    farm_entity = person.farm_entity 

    try:
        with transaction.atomic():
            customer.delete()  
            person.delete()  
            farm_entity.delete() 

            messages.error(request, "Customer deleted successfully!")
            return redirect("/customer")
    except Exception as e:
        messages.error(request, f"Error deleting customer: {str(e)}")
        return redirect("/customer")

@login_required(login_url='login')
def add_customer_contact(request):
    if not request.user.has_perm('erp.add_farmentitycontact'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method == 'POST':
        ccustomer_id = request.POST.get('customer_id')
        ccontact_type = request.POST.get('contact_type')
        ccontact = request.POST.get('contact')
            
        contact = FarmEntityContact(
            farm_entity_id=ccustomer_id,
            contact_type_id=ccontact_type,
            contact=ccontact
        )
        contact.save()

        messages.success(request, "Customer Contact Added Successfully!")
        return redirect("/customer")

    return render(request, 'sales/customer_edit.html')

@login_required(login_url='login')
def add_customer_address(request):
    if not request.user.has_perm('erp.add_farmentityaddress'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method == 'POST':
        ccustomer_id = request.POST.get('customer_id')
        cregion = request.POST.get('region')
        ccountry = request.POST.get('country')
        czone_subcity = request.POST.get('zone_subcity')
        cworeda = request.POST.get('woreda')
        ckebele = request.POST.get('kebele')
        chouse_no = request.POST.get('house_no')
        cstreet = request.POST.get('street')
            
        address = FarmEntityAddress(
            farm_entity_id=ccustomer_id,
            region_id=cregion,
            country=ccountry,
            zone_subcity=czone_subcity,
            woreda=cworeda,
            kebele=ckebele,
            house_number=chouse_no,
            street_name=cstreet,
        )
        address.save()

        messages.success(request, "Customer Address Added Successfully!")
        return redirect("/customer")

    return render(request, 'sales/customer_edit.html')
    
def get_item_types(request, item_id):
    try:
        stock_items = Stock.objects.filter(item_id=item_id).select_related('type')
        item_types_set = set()  # Use a set to store unique item types

        for stock_item in stock_items:
            if stock_item.type:
                item_type = (stock_item.type.item_type_id, stock_item.type.item_type)
                item_types_set.add(item_type)

        item_types = [{'id': item_type[0], 'name': item_type[1]} for item_type in item_types_set]

        return JsonResponse(item_types, safe=False)
    except Exception as e:
        print(f"Error in get_item_types: {e}")
        return JsonResponse({'error': str(e)}, status=500)
    
def get_item_measurements(request, item_id):
    try:
        stock_items = Stock.objects.filter(item_id=item_id).select_related('item_measurement')
        item_measurements_set = set()  # Use a set to store unique item measurements

        for stock_item in stock_items:
            if stock_item.item_measurement:
                item_measurement = (stock_item.item_measurement.id, stock_item.item_measurement.measurement)
                item_measurements_set.add(item_measurement)

        measurement_types = [{'id': item_measurement[0], 'name': item_measurement[1]} for item_measurement in item_measurements_set]

        return JsonResponse(measurement_types, safe=False)
    except Exception as e:
        print(f"Error in get_item_measurements: {e}")
        return JsonResponse({'error': str(e)}, status=500)

    
# def get_stock_quantity(request, item_id, type_id):
#     try:
#         stock_item = Stock.objects.get(item_id=item_id, type_id=type_id)
#         quantity = stock_item.quantity
#         return JsonResponse({'quantity': quantity})
#     except Stock.DoesNotExist:
#         return JsonResponse({'error': 'Stock not found'}, status=404)
def get_stock_quantity(request, item_id, type_id, item_measurement_id):
    try:
        stock_item = Stock.objects.get(item_id=item_id, type_id=type_id, item_measurement_id=item_measurement_id)
        quantity = stock_item.quantity
        return JsonResponse({'quantity': quantity})
    except Stock.DoesNotExist:
        return JsonResponse({'error': 'Stock not found'}, status=404)


@login_required(login_url='login')
def sales_order(request):
    if not request.user.has_perm('erp.view_salesorder'):
        return HttpResponse('You are not authorised to view this page', status=403)
    data = SalesOrder.objects.all()
    paginated_data = paginate_data(request, data, 10) 
    context = {
        "data1":paginated_data,
    }

    return render(request, 'sales/sales_order.html', context)

@login_required(login_url='login')
def sales_order_add(request):
    if not request.user.has_perm('erp.add_salesorder'):
        return HttpResponse('You are not authorised to view this page', status=403)

    if request.method == "POST":
        citem_name = request.POST.get('item_name')
        citem_type = request.POST.get('item_type')
        citem_measurement_id = request.POST.get('item_measurement_id')
        ccustomer_id = request.POST.get('customer_id')
        cquantity = request.POST.get('quantity')
        corder_date = request.POST.get('order_date')
        cunit_price = request.POST.get('unit_price')
        cpayment_method = request.POST.get('payment_method')
        cpayment_status = request.POST.get('payment_status')

        errors = []
        if cquantity:
            try:
                cquantity = float(cquantity)
                if cquantity <= 0:
                    errors.append("Quantity must be a positive number.")
            except ValueError:
                errors.append("Quantity must be a valid number.")
        else:
            errors.append("Quantity is required.")

        if corder_date:
            try:
                corder_date = datetime.strptime(corder_date, '%Y-%m-%dT%H:%M')
            except ValueError:
                errors.append('Order Date must be in YYYY-MM-DDTHH:MM format.')
        else:
            errors.append("Order Date is required.")

        if cunit_price:
            try:
                cunit_price = float(cunit_price)
                if cunit_price <= 0:
                    errors.append("Price must be a positive number.")
            except ValueError:
                errors.append('Price must be a number.')
        else:
            errors.append("Price is required.")

        if errors:
            context = {
                'errors': errors,
                'data1': Stock.objects.values('item_id', 'item__name').distinct(),
                'data2': Customer.objects.all(),
                'data3': PaymentMethod.objects.all(),
                'data4': ItemType.objects.all(),
            }
            return render(request, 'sales/sales_order_add.html', context)

        try:
            stock_instance = Stock.objects.get(item_id=citem_name, type_id=citem_type, item_measurement_id=citem_measurement_id)

            if float(stock_instance.quantity) < cquantity:
                errors.append("Order quantity exceeds available stock.")
                context = {
                    'errors': errors,
                    'data1': Stock.objects.values('item_id', 'item__name').distinct(),
                    'data2': Customer.objects.all(),
                    'data3': PaymentMethod.objects.all(),
                    'data4': ItemType.objects.all(),
                }
                return render(request, 'sales/sales_order_add.html', context)

            query = SalesOrder(
                stock=stock_instance,
                customer_id=ccustomer_id,
                quantity=cquantity,
                order_date=corder_date,
                unit_price=cunit_price,
                payment_method_id=cpayment_method,
                payment_status=cpayment_status,
                total_amount=cquantity * cunit_price,
                item_name=stock_instance.item.name, 
                item_type=stock_instance.type.item_type, 
                item_measurement=stock_instance.item_measurement.measurement 
            )
            query.save()

            stock_instance.quantity = str(float(stock_instance.quantity) - cquantity)
            if float(stock_instance.quantity) <= 0.0:
                stock_instance.delete()
            else:
                stock_instance.save()

            messages.success(request, "Sales Order Added Successfully!")
            return redirect("/sales_order")

        except Stock.DoesNotExist:
            errors.append("Stock item does not exist.")
            context = {
                'errors': errors,
                'data1': Stock.objects.values('item_id', 'item__name').distinct(),
                'data2': Customer.objects.all(),
                'data3': PaymentMethod.objects.all(),
                'data4': ItemType.objects.all(),
            }
            return render(request, 'sales/sales_order_add.html', context)
        except Exception as e:
            errors.append(f"An unexpected error occurred: {e}")
            context = {
                'errors': errors,
                'data1': Stock.objects.values('item_id', 'item__name').distinct(),
                'data2': Customer.objects.all(),
                'data3': PaymentMethod.objects.all(),
                'data4': ItemType.objects.all(),
            }
            return render(request, 'sales/sales_order_add.html', context)

    data1 = Stock.objects.values('item_id', 'item__name').distinct()
    data2 = Customer.objects.all()
    data3 = PaymentMethod.objects.all()
    data4 = ItemType.objects.all()
    context = {
        'data1': data1,
        'data2': data2,
        'data3': data3,
        'data4': data4,
    }

    return render(request, 'sales/sales_order_add.html', context)


# def sales_order_add(request):
#     if not request.user.has_perm('erp.add_salesorder'):
#         return HttpResponse('You are not authorised to view this page', status=403)

#     if request.method == "POST":
#         citem_name = request.POST.get('item_name')
#         citem_type = request.POST.get('item_type')
#         citem_measurement_id = request.POST.get('item_measurement_id')
#         ccustomer_id = request.POST.get('customer_id')
#         cquantity = request.POST.get('quantity')
#         corder_date = request.POST.get('order_date')
#         cunit_price = request.POST.get('unit_price')
#         cpayment_method = request.POST.get('payment_method')
#         cpayment_status = request.POST.get('payment_status')

#         errors = []
#         if cquantity:
#             try:
#                 cquantity = float(cquantity)
#                 if cquantity <= 0:
#                     errors.append("Quantity must be a positive number.")
#             except ValueError:
#                 errors.append("Quantity must be a valid number.")
#         else:
#             errors.append("Quantity is required.")

#         if corder_date:
#             try:
#                 corder_date = datetime.strptime(corder_date, '%Y-%m-%dT%H:%M')
#             except ValueError:
#                 errors.append('Order Date must be in YYYY-MM-DDTHH:MM format.')
#         else:
#             errors.append("Order Date is required.")

#         if cunit_price:
#             try:
#                 cunit_price = float(cunit_price)
#                 if cunit_price <= 0:
#                     errors.append("Price must be a positive number.")
#             except ValueError:
#                 errors.append('Price must be a number.')
#         else:
#             errors.append("Price is required.")

#         if errors:
#             context = {
#                 'errors': errors,
#                 'data1': Stock.objects.values('item_id', 'item__name').distinct(),
#                 'data2': Customer.objects.all(),
#                 'data3': PaymentMethod.objects.all(),
#                 'data4': ItemType.objects.all(),
#             }
#             return render(request, 'sales/sales_order_add.html', context)

#         try:
#             stock_instance = Stock.objects.get(item_id=citem_name, type_id=citem_type, item_measurement_id=citem_measurement_id)

#             if float(stock_instance.quantity) < cquantity:
#                 errors.append("Order quantity exceeds available stock.")
#                 context = {
#                     'errors': errors,
#                     'data1': Stock.objects.values('item_id', 'item__name').distinct(),
#                     'data2': Customer.objects.all(),
#                     'data3': PaymentMethod.objects.all(),
#                     'data4': ItemType.objects.all(),
#                 }
#                 return render(request, 'sales/sales_order_add.html', context)

#             query = SalesOrder(
#                 stock=stock_instance,
#                 customer_id=ccustomer_id,
#                 quantity=cquantity,
#                 order_date=corder_date,
#                 unit_price=cunit_price,
#                 payment_method_id=cpayment_method,
#                 payment_status=cpayment_status,
#                 total_amount=cquantity * cunit_price
#             )
#             query.save()

#             stock_instance.quantity = str(float(stock_instance.quantity) - cquantity)
#             if float(stock_instance.quantity) <= 0.0:
#                 stock_instance.delete()
#             else:
#                 stock_instance.save()

#             messages.success(request, "Sales Order Added Successfully!")
#             return redirect("/sales_order")

#         except Stock.DoesNotExist:
#             errors.append("Stock item does not exist.")
#             context = {
#                 'errors': errors,
#                 'data1': Stock.objects.values('item_id', 'item__name').distinct(),
#                 'data2': Customer.objects.all(),
#                 'data3': PaymentMethod.objects.all(),
#                 'data4': ItemType.objects.all(),
#             }
#             return render(request, 'sales/sales_order_add.html', context)
#         except Exception as e:
#             errors.append(f"An unexpected error occurred: {e}")
#             context = {
#                 'errors': errors,
#                 'data1': Stock.objects.values('item_id', 'item__name').distinct(),
#                 'data2': Customer.objects.all(),
#                 'data3': PaymentMethod.objects.all(),
#                 'data4': ItemType.objects.all(),
#             }
#             return render(request, 'sales/sales_order_add.html', context)

#     data1 = Stock.objects.values('item_id', 'item__name').distinct()
#     data2 = Customer.objects.all()
#     data3 = PaymentMethod.objects.all()
#     data4 = ItemType.objects.all()
#     context = {
#         'data1': data1,
#         'data2': data2,
#         'data3': data3,
#         'data4': data4,
#     }

#     return render(request, 'sales/sales_order_add.html', context)

@login_required(login_url='login')
def sales_order_edit(request, id):
    if not request.user.has_perm('erp.change_salesorder'):
        return HttpResponse('You are not authorised to view this page', status=403)
    
    edit = SalesOrder.objects.get(id=id)

    if request.method == "POST":
        ccustomer_id = request.POST.get('customer_id')
        cquantity = request.POST.get('quantity')
        corder_date = request.POST.get('order_date')
        cunit_price = request.POST.get('unit_price')
        cpayment_method = request.POST.get('payment_method')
        cpayment_status = request.POST.get('payment_status')

        errors = []
        if cquantity:
            try:
                cquantity = float(cquantity)
                if cquantity <= 0:
                    errors.append("Quantity must be a positive number.")
            except ValueError:
                errors.append("Quantity must be a valid number.")
        else:
            errors.append("Quantity is required.")

        if corder_date:
            try:
                corder_date = datetime.strptime(corder_date, '%Y-%m-%dT%H:%M')
            except ValueError:
                errors.append('Order Date must be in YYYY-MM-DDTHH:MM format.')
        else:
            errors.append("Order Date is required.")

        if cunit_price:
            try:
                cunit_price = float(cunit_price)
                if cunit_price <= 0:
                    errors.append("Price must be a positive number.")
            except ValueError:
                errors.append('Price must be a number.')
        else:
            errors.append("Price is required.")

        if errors:
            context = {
                'errors': errors,
                'd': edit,
                'data1': Stock.objects.all(),
                'data2': Customer.objects.all(),
                'data3': PaymentMethod.objects.all(),
            }
            return render(request, 'sales/sales_order_edit.html', context)
        
        ctotal_amount = cquantity * cunit_price

        stock_instance = edit.stock
        current_stock_quantity = float(stock_instance.quantity) if stock_instance else 0
        old_order_quantity = edit.quantity
        new_order_quantity = cquantity

        if current_stock_quantity + old_order_quantity - new_order_quantity < 0:
            errors.append("Order quantity exceeds available stock.")
            context = {
                'errors': errors,
                'd': edit,
                'data1': Stock.objects.all(),
                'data2': Customer.objects.all(),
                'data3': PaymentMethod.objects.all(),
            }
            return render(request, 'sales/sales_order_edit.html', context)

        if stock_instance:
            stock_instance.quantity = str(current_stock_quantity + old_order_quantity - new_order_quantity)
            stock_instance.save()

        edit.customer_id = ccustomer_id
        edit.quantity = cquantity
        edit.order_date = corder_date
        edit.unit_price = cunit_price
        edit.payment_method_id = cpayment_method
        edit.payment_status = cpayment_status
        edit.total_amount = ctotal_amount
        edit.save()

        if stock_instance and float(stock_instance.quantity) == 0.0:
            stock_instance.delete()

        messages.success(request, "Sales Order updated Successfully!")
        return redirect("/sales_order")
    
    d = edit
    data1 = Stock.objects.all()
    data2 = Customer.objects.all()
    data3 = PaymentMethod.objects.all()
    context = {
        "d": d,
        'data1': data1,
        'data2': data2,
        'data3': data3,
    }
    return render(request, 'sales/sales_order_edit.html', context)


def sales_order_delete(request, id):
    if not request.user.has_perm('erp.delete_salesorder'):
        return HttpResponse('You are not authorised to view this page', status=403)
    d = SalesOrder.objects.get(id=id)
    d.delete()
    messages.error(request, "Sales Order Deleted Successfully!")
    return redirect("/sales_order")

@login_required(login_url='login')
def region(request):
    if not request.user.has_perm('erp.view_region'):
        return HttpResponse('You are not authorised to view this page', status=403)
    data = Region.objects.all()
    paginated_data = paginate_data(request, data, 10) 
    context = {"data1":paginated_data}

    return render(request, 'person/region.html', context)

@login_required(login_url='login')
def region_add(request):
    if not request.user.has_perm('erp.add_region'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method=="POST":
        cregion=request.POST.get('region')
        cdate = datetime.now().date()

        query = Region(region=cregion, modified_date=cdate)
        query.save()
        messages.success(request, "Region Added Successfully!")
        return redirect("/region")

    return render(request, 'person/region_add.html')

@login_required(login_url='login')
def region_edit(request,region_id):
    if not request.user.has_perm('erp.change_region'):
        return HttpResponse('You are not authorised to view this page', status=403)
    edit = Region.objects.get(region_id=region_id)
    
    if request.method == "POST":
        cregion=request.POST.get('region')
        cdate = datetime.now().date()
        
        edit.region = cregion
        edit.modified_date = cdate
        
        edit.save()
        messages.warning(request, "Region Updated Successfully!")
        return redirect("/region")

    d = Region.objects.get(region_id=region_id)
    context = {"d": d}

    return render(request, 'person/region_edit.html', context)

def region_delete(request, region_id):
    if not request.user.has_perm('erp.delete_region'):
        return HttpResponse('You are not authorised to view this page', status=403)
    d = Region.objects.get(region_id=region_id)
    d.delete()
    messages.error(request, "Region Deleted Successfully!")
    return redirect("/region")

@login_required(login_url='login')
def guarantee_type(request):
    if not request.user.has_perm('erp.view_guaranteetype'):
        return HttpResponse('You are not authorised to view this page', status=403)
    data = GuaranteeType.objects.all()
    paginated_data = paginate_data(request, data, 10) 
    context = {"data1":paginated_data}

    return render(request, 'employee/guarantee_type.html', context)

@login_required(login_url='login')
def guarantee_type_add(request):
    if not request.user.has_perm('erp.add_guaranteetype'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method=="POST":
        cguarantee_type=request.POST.get('guarantee_type')
        cdate = datetime.now().date()

        query = GuaranteeType(guarantee_type=cguarantee_type, modified_date=cdate)
        query.save()
        messages.success(request, "Guarantee Type Added Successfully!")
        return redirect("/guarantee_type")

    return render(request, 'employee/guarantee_type_add.html')

@login_required(login_url='login')
def guarantee_type_edit(request,guarantee_type_id):
    if not request.user.has_perm('erp.change_guaranteetype'):
        return HttpResponse('You are not authorised to view this page', status=403)
    edit = GuaranteeType.objects.get(guarantee_type_id=guarantee_type_id)
    
    if request.method == "POST":
        cguarantee_type=request.POST.get('guarantee_type')
        cdate = datetime.now().date()
        
        edit.guarantee_type = cguarantee_type
        edit.modified_date = cdate
        
        edit.save()
        messages.warning(request, "Guarantee Type Updated Successfully!")
        return redirect("/guarantee_type")

    d = GuaranteeType.objects.get(guarantee_type_id=guarantee_type_id)
    context = {"d": d}

    return render(request, 'employee/guarantee_type_edit.html', context)

def guarantee_type_delete(request, guarantee_type_id):
    if not request.user.has_perm('erp.delete_guaranteetype'):
        return HttpResponse('You are not authorised to view this page', status=403)
    d = GuaranteeType.objects.get(guarantee_type_id=guarantee_type_id)
    d.delete()
    messages.error(request, "Guarantee Type Deleted Successfully!")
    return redirect("/guarantee_type")

@login_required(login_url='login')
def shift(request):
    if not request.user.has_perm('erp.view_shift'):
        return HttpResponse('You are not authorised to view this page', status=403)
    data = Shift.objects.all()
    paginated_data = paginate_data(request, data, 10) 
    context = {"data1":paginated_data}

    return render(request, 'employee/shift.html', context)

@login_required(login_url='login')
def shift_add(request):
    if not request.user.has_perm('erp.add_shift'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method=="POST":
        cshift_name=request.POST.get('shift_name')
        cshift_start_time=request.POST.get('shift_start_time')
        cshift_end_time=request.POST.get('shift_end_time')
        cdate = datetime.now().date()

        errors = []
        if cshift_start_time:
            try:
                cshift_start_time = datetime.strptime(cshift_start_time, '%Y-%m-%dT%H:%M')
            except ValueError:
                errors.append('Invalid Start Time format. Use YYYY-MM-DDTHH:MM format.')
        else:
            cshift_start_time = None 

        if cshift_end_time:
            try:
                cshift_end_time = datetime.strptime(cshift_end_time, '%Y-%m-%dT%H:%M')
            except ValueError:
                errors.append('Invalid End Time format. Use YYYY-MM-DDTHH:MM format.')
        else:
            cshift_end_time = None 

        if errors:
            context = {
                'errors': errors,
            }
            return render(request, 'employee/shift_add.html', context)

        query = Shift(shift_name=cshift_name, shift_start_time=cshift_start_time, shift_end_time=cshift_end_time,modified_date=cdate)
        query.save()
        messages.success(request, "Shift Added Successfully!")
        return redirect("/shift")

    return render(request, 'employee/shift_add.html')

@login_required(login_url='login')
def shift_edit(request,id):
    if not request.user.has_perm('erp.change_shift'):
        return HttpResponse('You are not authorised to view this page', status=403)
    edit = Shift.objects.get(id=id)
    
    if request.method == "POST":
        cshift_name=request.POST.get('shift_name')
        cshift_start_time=request.POST.get('shift_start_time')
        cshift_end_time=request.POST.get('shift_end_time')
        cdate = datetime.now().date()

        errors = []
        if cshift_start_time:
            try:
                cshift_start_time = datetime.strptime(cshift_start_time, '%Y-%m-%dT%H:%M')
            except ValueError:
                errors.append('Invalid Start Time format. Use YYYY-MM-DDTHH:MM format.')
        else:
            cshift_start_time = None 

        if cshift_end_time:
            try:
                cshift_end_time = datetime.strptime(cshift_end_time, '%Y-%m-%dT%H:%M')
            except ValueError:
                errors.append('Invalid End Time format. Use YYYY-MM-DDTHH:MM format.')
        else:
            cshift_end_time = None 

        if errors:
            context = {
                'errors': errors,
                'd': Shift.objects.get(id=id)
            }
            return render(request, 'employee/shift_edit.html', context)
        
        edit.shift_name = cshift_name
        edit.shift_start_time = cshift_start_time
        edit.shift_end_time = cshift_end_time
        edit.modified_date=cdate
        
        edit.save()
        messages.warning(request, "Shift Updated Successfully!")
        return redirect("/shift")

    d = Shift.objects.get(id=id)
    context = {"d": d}

    return render(request, 'employee/shift_edit.html', context)

def shift_delete(request, id):
    if not request.user.has_perm('erp.delete_shift'):
        return HttpResponse('You are not authorised to view this page', status=403)
    d = Shift.objects.get(id=id)
    d.delete()
    messages.error(request, "Shift Deleted Successfully!")
    return redirect("/shift")


@login_required(login_url='login')
def task(request):
    if not request.user.has_perm('erp.view_task'):
        return HttpResponse('You are not authorised to view this page', status=403)
    data = Task.objects.all()
    paginated_data = paginate_data(request, data, 10) 
    context = {"data1":paginated_data}

    return render(request, 'employee/task.html', context)

@login_required(login_url='login')
def task_add(request):
    if not request.user.has_perm('erp.add_task'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method=="POST":
        ctask_name=request.POST.get('task_name')
        cdescription=request.POST.get('description')
        cdate = datetime.now().date()

        query = Task(task_name=ctask_name, description=cdescription, modified_date=cdate)
        query.save()
        messages.success(request, "Task Added Successfully!")
        return redirect("/task")

    return render(request, 'employee/task_add.html')

@login_required(login_url='login')
def task_edit(request,id):
    if not request.user.has_perm('erp.change_task'):
        return HttpResponse('You are not authorised to view this page', status=403)
    edit = Task.objects.get(id=id)
    
    if request.method == "POST":
        ctask_name=request.POST.get('task_name')
        cdescription=request.POST.get('description')
        cdate = datetime.now().date()
        
        edit.task_name = ctask_name
        edit.description = cdescription
        edit.modified_date = cdate
        
        edit.save()
        messages.warning(request, "Task Updated Successfully!")
        return redirect("/task")

    d = Task.objects.get(id=id)
    context = {"d": d}

    return render(request, 'employee/task_edit.html', context)

def task_delete(request, id):
    if not request.user.has_perm('erp.delete_task'):
        return HttpResponse('You are not authorised to view this page', status=403)
    d = Task.objects.get(id=id)
    d.delete()
    messages.error(request, "Task Deleted Successfully!")
    return redirect("/task")

@login_required(login_url='login')
def assign_task(request):
    if not request.user.has_perm('erp.view_taskassignment'):
        return HttpResponse('You are not authorised to view this page', status=403)
    user = request.user
    if request.user.has_perm('erp.add_taskassignment'):
        data = TaskAssignment.objects.all()
    else:
        user_profile = get_object_or_404(UserProfile, user=user)
        assigned_person = user_profile.employee
        data = TaskAssignment.objects.filter(assigned_to=assigned_person)

    paginated_data = paginate_data(request, data, 10) 

    task_data = Task.objects.all()
    shift_data = Shift.objects.all()
    employee_data = Employee.objects.all()

    context = {"data1":paginated_data,'task_data': task_data,'shift_data': shift_data, 'employee_data': employee_data}

    return render(request, 'employee/assign_task.html', context)

@login_required(login_url='login')
def assign_task_add(request):
    if not request.user.has_perm('erp.add_taskassignment'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method=="POST":
        ctask_id=request.POST.get('task_id')
        cshift_id=request.POST.get('shift_id')
        cassigned_to_id=request.POST.get('assigned_to_id')
        cdue_time=request.POST.get('due_time')

        errors = []
        if cdue_time:
            try:
                cdue_time = datetime.strptime(cdue_time, '%Y-%m-%dT%H:%M')
            except ValueError:
                errors.append('Invalid Due Time format. Use YYYY-MM-DDTHH:MM format.')
        else:
            cdue_time = None 
            
        if errors:
            context = {
                'errors': errors,
                'data1': Task.objects.all(),
                'data2': Shift.objects.all(),
                'data3': Employee.objects.all(),

            }
            return render(request, 'employee/assign_task_add.html', context)

        query = TaskAssignment.objects.create(task_id=ctask_id, shift_id=cshift_id, assigned_to_id=cassigned_to_id, due_time=cdue_time)
        query.save()
        messages.success(request, "Task Assignment Added Successfully!")
        return redirect("/assign_task")
     
    task_data = Task.objects.all()
    shift_data = Shift.objects.all()
    employee_data = Employee.objects.all()
    context = {
        'data1': task_data,
        'data2': shift_data,
        'data3': employee_data,
    }

    return render(request, 'employee/assign_task_add.html', context)

@login_required(login_url='login')
def assign_task_edit(request,id):
    if not request.user.has_perm('erp.change_taskassignment'):
        return HttpResponse('You are not authorised to view this page', status=403)
    edit = TaskAssignment.objects.get(id=id)
    if request.method=="POST":
        ctask_id=request.POST.get('task_id')
        cshift_id=request.POST.get('shift_id')
        cassigned_to_id=request.POST.get('assigned_to_id')
        cdue_time=request.POST.get('due_time')

        errors = []
        if cdue_time:
            try:
                cdue_time = datetime.strptime(cdue_time, '%Y-%m-%dT%H:%M')
            except ValueError:
                errors.append('Invalid Due Time format. Use YYYY-MM-DDTHH:MM format.')
        else:
            cdue_time = None 
            
        if errors:
            context = {
                'errors': errors,
                'd': TaskAssignment.objects.get(id=id),
                'data1': Task.objects.all(),
                'data2': Shift.objects.all(),
                'data3': Employee.objects.all(),

            }
            return render(request, 'employee/assign_task_edit.html', context)

        edit.task_id = ctask_id
        edit.shift_id = cshift_id
        edit.assigned_to_id = cassigned_to_id
        edit.due_time = cdue_time
        
        edit.save()
        messages.warning(request, "Assigned Task Updated Successfully!")
        return redirect("/assign_task")

    d = TaskAssignment.objects.get(id=id)
    task_data = Task.objects.all()
    shift_data = Shift.objects.all()
    employee_data = Employee.objects.all()
    context = {'d': d,'data1': task_data,'data2': shift_data,'data3': employee_data,}

    return render(request, 'employee/assign_task_edit.html', context)

def assign_task_delete(request, id):
    if not request.user.has_perm('erp.delete_taskassignment'):
        return HttpResponse('You are not authorised to view this page', status=403)
    d = TaskAssignment.objects.get(id=id)
    d.delete()
    messages.error(request, "Task Assignment Deleted Successfully!")
    return redirect("/assign_task")

def update_status(request):
    if request.method == 'POST':
        task_id = request.POST.get('id')
        status = request.POST.get('status')
        original_status = request.POST.get('original_status')

        try:
            task = get_object_or_404(TaskAssignment, pk=task_id)

            if status == 'Completed' and original_status == 'Rejected':
                task.status = 'Reassigned'
                task.approval_status = None
            else:
                task.status = status
                print(f'Status set to {status}')  

            task.save()
            messages.success(request, 'Status updated successfully.')
            return redirect('/assign_task')
        except TaskAssignment.DoesNotExist:
            messages.error(request, 'Invalid request method.')
            return redirect('/assign_task')
        
    else:
        messages.error(request, 'Invalid request method.')
        return redirect('/assign_task') 
    
def add_rating(request):
     if request.method == 'POST':
        task_id = request.POST.get('id')
        rating = request.POST.get('rating')

        if not task_id:
            messages.error(request, 'Task ID is missing.')
            return redirect('/assign_task')

        task = get_object_or_404(TaskAssignment, pk=task_id)
        task.rating = rating   
        task.save()

        messages.success(request, 'Rate Added successfully.')
        return redirect('/assign_task')
    
def approve_task(request, id):
    try:
        task = TaskAssignment.objects.get(pk=id)
        task.approval_status = 'Approved'
        task.save()
        return JsonResponse({'message': 'Task Approved successfully.'})
    except EmployeeLeave.DoesNotExist:
        return JsonResponse({'error': 'Task not found.'}, status=404)


def reject_task(request, id):
    try:
        task = TaskAssignment.objects.get(pk=id)
        task.approval_status = 'Rejected'
        task.save()
        return JsonResponse({'message': 'Task Rejected successfully.'})
    except EmployeeLeave.DoesNotExist:
        return JsonResponse({'error': 'Task not found.'}, status=404)
  

@login_required(login_url='login')
def job(request):
    if not request.user.has_perm('erp.view_job'):
        return HttpResponse('You are not authorised to view this page', status=403)
    data = Job.objects.all()
    paginated_data = paginate_data(request, data, 10) 
    context = {"data1":paginated_data}

    return render(request, 'employee/job.html', context)

@login_required(login_url='login')
def job_add(request):
    if not request.user.has_perm('erp.add_job'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method=="POST":
        cjob_title=request.POST.get('job_title')
        cjob_min_salary=request.POST.get('job_min_salary')
        cjob_max_salary=request.POST.get('job_max_salary')

        errors = []
        if cjob_min_salary:
            try:
                cjob_min_salary = float(cjob_min_salary)
                if cjob_min_salary <= 0:
                    errors.append("Salary must be a positive number.")
            except ValueError:
                errors.append('Minimum Salary must be a number.')
        else:
            cjob_min_salary = None 

        if cjob_max_salary:
            try:
                cjob_max_salary = float(cjob_max_salary)
                if cjob_max_salary <= 0:
                    errors.append("Salary must be a positive number.")
            except ValueError:
                errors.append('Maximum Salary must be a number.')
        else:
            cjob_max_salary = None 

        if errors:
            context = {
                'errors': errors,
            }
            return render(request, 'employee/job_add.html', context)

        query = Job(job_title=cjob_title, job_min_salary=cjob_min_salary, job_max_salary=cjob_max_salary)
        query.save()
        messages.success(request, "Job Added Successfully!")
        return redirect("/job")

    return render(request, 'employee/job_add.html')

@login_required(login_url='login')
def job_edit(request,job_id):
    if not request.user.has_perm('erp.change_job'):
        return HttpResponse('You are not authorised to view this page', status=403)
    edit = Job.objects.get(job_id=job_id)
    
    if request.method == "POST":
        cjob_title=request.POST.get('job_title')
        cjob_min_salary=request.POST.get('job_min_salary')
        cjob_max_salary=request.POST.get('job_max_salary')

        errors = []
        if cjob_min_salary:
            try:
                cjob_min_salary = float(cjob_min_salary)
                if cjob_min_salary <= 0:
                    errors.append("Salary must be a positive number.")
            except ValueError:
                errors.append('Minimum Salary must be a number.')
        else:
            cjob_min_salary = None 

        if cjob_max_salary:
            try:
                cjob_max_salary = float(cjob_max_salary)
                if cjob_max_salary <= 0:
                    errors.append("Salary must be a positive number.")
            except ValueError:
                errors.append('Maximum Salary must be a number.')
        else:
            cjob_max_salary = None 

        if errors:
            context = {
                'd':Job.objects.get(job_id=job_id),
                'errors': errors,
            }
            return render(request, 'employee/job_edit.html', context)
        
        edit.job_title = cjob_title
        edit.job_min_salary = cjob_min_salary
        edit.job_max_salary = cjob_max_salary
        
        edit.save()
        messages.warning(request, "Job Updated Successfully!")
        return redirect("/job")

    d = Job.objects.get(job_id=job_id)
    context = {"d": d}

    return render(request, 'employee/job_edit.html', context)

def job_delete(request, job_id):
    if not request.user.has_perm('erp.delete_job'):
        return HttpResponse('You are not authorised to view this page', status=403)
    d = Job.objects.get(job_id=job_id)
    d.delete()
    messages.error(request, "Job Deleted Successfully!")
    return redirect("/job")


@login_required(login_url='login')
def item_type(request):
    if not request.user.has_perm('erp.view_itemtype'):
        return HttpResponse('You are not authorised to view this page', status=403)
    data = ItemType.objects.all()
    paginated_data = paginate_data(request, data, 10) 
    context = {"data1":paginated_data}

    return render(request, 'procurement/item_type.html', context)

@login_required(login_url='login')
def item_type_add(request):
    if not request.user.has_perm('erp.add_itemtype'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method=="POST":
        citem_type=request.POST.get('item_type')
        cdate = datetime.now().date()

        query = ItemType(item_type=citem_type, modified_date=cdate)
        query.save()
        messages.success(request, "Item Type Added Successfully!")
        return redirect("/item_type")

    return render(request, 'procurement/item_type_add.html')

@login_required(login_url='login')
def item_type_edit(request,item_type_id):
    if not request.user.has_perm('erp.change_itemtype'):
        return HttpResponse('You are not authorised to view this page', status=403)
    edit = ItemType.objects.get(item_type_id=item_type_id)
    
    if request.method == "POST":
        citem_type=request.POST.get('item_type')
        cdate = datetime.now().date()
        
        edit.item_type = citem_type
        edit.modified_date = cdate
        
        edit.save()
        messages.warning(request, "Item Type Updated Successfully!")
        return redirect("/item_type")

    d = ItemType.objects.get(item_type_id=item_type_id)
    context = {"d": d}

    return render(request, 'procurement/item_type_edit.html', context)

def item_type_delete(request, item_type_id):
    if not request.user.has_perm('erp.delete_itemtype'):
        return HttpResponse('You are not authorised to view this page', status=403)
    d = ItemType.objects.get(item_type_id=item_type_id)
    d.delete()
    messages.error(request, "Item Type Deleted Successfully!")
    return redirect("/item_type")

@login_required(login_url='login')
def item(request):
    if not request.user.has_perm('erp.view_item'):
        return HttpResponse('You are not authorised to view this page', status=403)
    data = Item.objects.all()
    paginated_data = paginate_data(request, data, 10) 
    context = {"data1":paginated_data}

    return render(request, 'procurement/item.html', context)

@login_required(login_url='login')
def item_add(request):
    if not request.user.has_perm('erp.add_item'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method=="POST":
        cname=request.POST.get('name')
        cdate = datetime.now().date()

        query = Item(name=cname, modified_date=cdate)
        query.save()
        messages.success(request, "Item Added Successfully!")
        return redirect("/item")

    return render(request, 'procurement/item_add.html')

@login_required(login_url='login')
def item_edit(request,item_id):
    if not request.user.has_perm('erp.change_item'):
        return HttpResponse('You are not authorised to view this page', status=403)
    edit = Item.objects.get(item_id=item_id)
    
    if request.method == "POST":
        cname=request.POST.get('name')
        cdate = datetime.now().date()
        
        edit.name = cname
        edit.modified_date = cdate
        
        edit.save()
        messages.warning(request, "Item Updated Successfully!")
        return redirect("/item")

    d = Item.objects.get(item_id=item_id)
    context = {"d": d}

    return render(request, 'procurement/item_edit.html', context)

def item_delete(request, item_id):
    if not request.user.has_perm('erp.delete_item'):
        return HttpResponse('You are not authorised to view this page', status=403)
    d = Item.objects.get(item_id=item_id)
    d.delete()
    messages.error(request, "Item Deleted Successfully!")
    return redirect("/item")

@login_required(login_url='login')
def supplier_type(request):
    if not request.user.has_perm('erp.view_suppliertype'):
        return HttpResponse('You are not authorised to view this page', status=403)
    data = SupplierType.objects.all()
    paginated_data = paginate_data(request, data, 10) 
    context = {"data1":paginated_data}

    return render(request, 'procurement/supplier_type.html', context)

@login_required(login_url='login')
def supplier_type_add(request):
    if not request.user.has_perm('erp.add_suppliertype'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method=="POST":
        csupplier_type=request.POST.get('supplier_type')
        cdate = datetime.now().date()

        query = SupplierType(supplier_type=csupplier_type, modified_date=cdate)
        query.save()
        messages.success(request, "Supplier Type Added Successfully!")
        return redirect("/supplier_type")

    return render(request, 'procurement/supplier_type_add.html')

@login_required(login_url='login')
def supplier_type_edit(request,supplier_type_id):
    if not request.user.has_perm('erp.change_suppliertype'):
        return HttpResponse('You are not authorised to view this page', status=403)
    edit = SupplierType.objects.get(supplier_type_id=supplier_type_id)
    
    if request.method == "POST":
        csupplier_type=request.POST.get('supplier_type')
        cdate = datetime.now().date()
        
        edit.supplier_type = csupplier_type
        edit.modified_date = cdate
        
        edit.save()
        messages.warning(request, "Supplier Type Updated Successfully!")
        return redirect("/supplier_type")

    d = SupplierType.objects.get(supplier_type_id=supplier_type_id)
    context = {"d": d}

    return render(request, 'procurement/supplier_type_edit.html', context)

def supplier_type_delete(request, supplier_type_id):
    if not request.user.has_perm('erp.delete_suppliertype'):
        return HttpResponse('You are not authorised to view this page', status=403)
    d = SupplierType.objects.get(supplier_type_id=supplier_type_id)
    d.delete()
    messages.error(request, "Supplier Type Deleted Successfully!")
    return redirect("/supplier_type")

from django.db.models import Q, Prefetch
@login_required(login_url='login')
def supplier(request):
    if not request.user.has_perm('erp.view_supplier'):
        return HttpResponse('You are not authorised to view this page', status=403)
    
    suppliers = Supplier.objects.all()
    phone_contacts = FarmEntityContact.objects.filter(contact_type__contact_type='Phone_Safaricom')
    phone_contacts2 = FarmEntityContact.objects.filter(contact_type__contact_type='Phone_Ethiotel')
    email_contacts = FarmEntityContact.objects.filter(contact_type__contact_type='Email')
    
    suppliers_with_contacts = suppliers.prefetch_related(
        Prefetch('farm_entity__farmentitycontact_set', queryset=phone_contacts, to_attr='phone_contacts'),
        Prefetch('farm_entity__farmentitycontact_set', queryset=phone_contacts2, to_attr='phone_contacts2'),
        Prefetch('farm_entity__farmentitycontact_set', queryset=email_contacts, to_attr='email_contacts')
    )
    paginated_data = paginate_data(request, suppliers_with_contacts, 10)
    
    type_data = SupplierType.objects.all()

    all_addresses = FarmEntityAddress.objects.all()

    address_dict = {}
    for address in all_addresses:
        if address.farm_entity_id not in address_dict:
            address_dict[address.farm_entity_id] = address

    address_data = list(address_dict.values())
    context = {
        "data1": paginated_data,
        'type_data': type_data,
        'address_data': address_data,
    }

    return render(request, 'procurement/supplier.html', context)

@login_required(login_url='login')
def supplier_add(request):
    if not request.user.has_perm('erp.add_supplier'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method == "POST":
        csupplier_name = request.POST.get('supplier_name')
        csupplier_type = request.POST.get('supplier_type')
        caccount_number = request.POST.get('account_number')

        farm_entity = FarmEntity.objects.create(modified_date=timezone.now())

        supplier = Supplier.objects.create(
            farm_entity=farm_entity,
            supplier_name=csupplier_name,
            supplier_type_id=csupplier_type,
            account_number=caccount_number
        )

        messages.success(request, "Supplier Added Successfully!")
        return redirect("/supplier")

    type_data = SupplierType.objects.all()
    context = {
        'data1': type_data,
    }

    return render(request, 'procurement/supplier_add.html', context)

@login_required(login_url='login')
def supplier_edit(request,farm_entity_id):
    if not request.user.has_perm('erp.change_supplier'):
        return HttpResponse('You are not authorised to view this page', status=403)
    edit = Supplier.objects.get(farm_entity_id=farm_entity_id)
    
    if request.method == "POST":
        csupplier_name = request.POST.get('supplier_name')
        csupplier_type = request.POST.get('supplier_type')
        caccount_number = request.POST.get('account_number')
        
        edit.supplier_name = csupplier_name
        edit.supplier_type_id = csupplier_type
        edit.account_number = caccount_number
        
        edit.save()
        messages.warning(request, "Supplier Updated Successfully!")
        return redirect("/supplier")

    d = Supplier.objects.get(farm_entity_id=farm_entity_id)
    data1 = SupplierType.objects.all()
    contact_data = ContactType.objects.all() 
    region_data = Region.objects.all() 

    context = {"d": d, "type": edit, "data1": data1, "data6": contact_data, 
        "data7": region_data,}

    return render(request, 'procurement/supplier_edit.html', context)

def supplier_delete(request, farm_entity_id):
    if not request.user.has_perm('erp.delete_supplier'):
        return HttpResponse('You are not authorised to view this page', status=403)
    d = Supplier.objects.get(farm_entity_id=farm_entity_id)
    d.delete()
    messages.error(request, "Supplier Deleted Successfully!")
    return redirect("/supplier")

@login_required(login_url='login')
def add_supplier_contact(request):
    if not request.user.has_perm('erp.add_farmentitycontact'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method == 'POST':
        csupplier_id = request.POST.get('supplier_id')
        ccontact_type = request.POST.get('contact_type')
        ccontact = request.POST.get('contact')
            
        contact = FarmEntityContact(
            farm_entity_id=csupplier_id,
            contact_type_id=ccontact_type,
            contact=ccontact
        )
        contact.save()

        messages.success(request, "Supplier Contact Added Successfully!")
        return redirect("/supplier")

    return render(request, 'procurement/supplier_edit.html')

@login_required(login_url='login')
def add_supplier_address(request):
    if not request.user.has_perm('erp.add_farmentityaddress'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method == 'POST':
        csupplier_id = request.POST.get('supplier_id')
        cregion = request.POST.get('region')
        ccountry = request.POST.get('country')
        czone_subcity = request.POST.get('zone_subcity')
        cworeda = request.POST.get('woreda')
        ckebele = request.POST.get('kebele')
        chouse_no = request.POST.get('house_no')
        cstreet = request.POST.get('street')
            
        address = FarmEntityAddress(
            farm_entity_id=csupplier_id,
            region_id=cregion,
            country=ccountry,
            zone_subcity=czone_subcity,
            woreda=cworeda,
            kebele=ckebele,
            house_number=chouse_no,
            street_name=cstreet,
        )
        address.save()

        messages.success(request, "Supplier Address Added Successfully!")
        return redirect("/supplier")

    return render(request, 'supplier/supplier_edit.html')

@login_required(login_url='login')
def request_order(request):
    if not request.user.has_perm('erp.view_order'):
        return HttpResponse('You are not authorised to view this page', status=403)
    data = OrderHasItem.objects.all()
    orderdatas = Order.objects.all()
    item_data = Item.objects.all()
    measurement_data = ItemMeasurement.objects.all()
    paginated_data = paginate_data(request, data, 10) 

    context = {"data1":paginated_data,'orderdatas': orderdatas,'item_data': item_data, 'measurement_data': measurement_data}

    return render(request, 'procurement/request_order.html', context)

@login_required(login_url='login')
def request_order_view(request, order_id):
    if not request.user.has_perm('erp.view_order'):
        return HttpResponse('You are not authorised to view this page', status=403)
    order = get_object_or_404(OrderHasItem, order_id=order_id)
    orderdatas = Order.objects.filter(order_id=order_id)
    rfq_data = OrderHasItemSupplier.objects.filter(order_id=order_id)

    context = {"order":order, 'orderdatas': orderdatas, "rfq_data": rfq_data}

    return render(request, 'procurement/request_order_view.html', context)


@login_required(login_url='login')
def request_order_add(request):
    if not request.user.has_perm('erp.add_order'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method=="POST":
        order = Order.objects.create()

        citem_name=request.POST.get('item_name')
        citem_type=request.POST.get('item_type')
        cquantity=request.POST.get('quantity')
        citem_measurement_id=request.POST.get('item_measurement_id')
        cdate=datetime.now().date()

        errors = []
        if cquantity:
            try:
                cquantity = float(cquantity)
                if cquantity <= 0:
                    errors.append("Quantity must be a positive number.")
            except ValueError:
                errors.append("Quantity must be a valid number.")
        else:
            cquantity = None

        if errors:
            context = {
                'errors': errors,
                'data1': Item.objects.all(),
                'data2': ItemMeasurement.objects.all(),
                'data3': ItemType.objects.all(),
            }
 
            return render(request, 'procurement/request_order_add.html', context)
        
        order.requested_date = datetime.now().date()
        order.request_approved = 'Pending'
        order.save()

        query = OrderHasItem.objects.create(order=order, item_id=citem_name, type_id=citem_type, item_measurement_id=citem_measurement_id, quantity=cquantity, modified_date=cdate)
        query.save()
        messages.success(request, "Order Request Added Successfully!")
        return redirect("/request_order")
     
    item_data = Item.objects.all()
    measurement_data = ItemMeasurement.objects.all()
    type_data = ItemType.objects.all()
    context = {
        'data1': item_data,
        'data2': measurement_data,
        'data3': type_data,
    }

    return render(request, 'procurement/request_order_add.html', context)

@login_required(login_url='login')
def request_order_edit(request,order_id):
    if not request.user.has_perm('erp.change_order'):
        return HttpResponse('You are not authorised to view this page', status=403)
    edit = OrderHasItem.objects.get(order_id=order_id)
    
    if request.method == "POST":
        citem_name=request.POST.get('item_name')
        citem_type=request.POST.get('item_type')
        citem_measurement_id=request.POST.get('item_measurement_id')
        cquantity=request.POST.get('quantity')
        cdate=datetime.now().date()

        errors = []
        if cquantity:
            try:
                cquantity = float(cquantity)
                if cquantity <= 0:
                    errors.append("Quantity must be a positive number.")
            except ValueError:
                errors.append("Quantity must be a valid number.")
        else:
            cquantity = None

        if errors:
            context = {
                'errors': errors,
                "d": OrderHasItem.objects.get(order_id=order_id), 
                "item": edit, 
                "data1": Item.objects.all(),
                "data2": ItemMeasurement.objects.all(),
                'data3': ItemType.objects.all(),
            }
 
            return render(request, 'procurement/request_order_edit.html', context)
        
        edit.item_id = citem_name
        edit.type_id = citem_type
        edit.item_measurement_id = citem_measurement_id
        edit.quantity = cquantity
        edit.modified_date = cdate
        edit.save()
        messages.warning(request, "Request Updated Successfully!")
        return redirect("/request_order")

    d = OrderHasItem.objects.get(order_id=order_id)
    data1 = Item.objects.all()
    data2 = ItemMeasurement.objects.all()
    type_data = ItemType.objects.all()
    context = {"d": d, "item": edit, "data1": data1, "data2": data2, 'data3': type_data,}

    return render(request, 'procurement/request_order_edit.html', context)

def request_order_delete(request, order_id):
    if not request.user.has_perm('erp.delete_order'):
        return HttpResponse('You are not authorised to view this page', status=403)
    try:
        order_item = OrderHasItem.objects.get(order_id=order_id)
        order = order_item.order
        order_item.delete()

        remaining_items = OrderHasItem.objects.filter(order=order)
        if remaining_items.count() == 0:
            order.delete()
        
        messages.error(request, "Request Deleted Successfully!")
    except OrderHasItem.DoesNotExist:
        messages.error(request, "Order not found!")
    
    return redirect("/request_order") 

def approve_request(request, order_id):
    try:
        order = Order.objects.get(pk=order_id)
        order.request_approved = 'Approved'
        order.request_approved_date = datetime.now().date()
        order.save()
        return JsonResponse({'message': 'Order request approved successfully.'})
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found.'}, status=404)

def reject_request(request, order_id):
    try:
        order = Order.objects.get(pk=order_id)
        order.request_approved = 'Rejected'
        order.request_approved_date = datetime.now().date()
        order.save()
        return JsonResponse({'message': 'Order request rejected successfully.'})
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found.'}, status=404)

@login_required(login_url='login')
def rfq(request):
    if not request.user.has_perm('erp.view_orderhasitemsupplier'):
        return HttpResponse('You are not authorised to view this page', status=403)
    data = OrderHasItemSupplier.objects.all()
    context = {"data1":data}

    return render(request, 'procurement/rfq.html', context)


@login_required(login_url='login')
def rfq_add(request, order_id):
    if not request.user.has_perm('erp.add_orderhasitemsupplier'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method == "POST":
        csupplier_name = request.POST.get('supplier_name')
        citem_id = request.POST.get('item_id')
        cquantity = request.POST.get('quantity')
        cprice = request.POST.get('price')
        cdate = datetime.now().date()

        errors = []
        if cquantity:
            try:
                cquantity = float(cquantity)
                if cquantity <= 0:
                    errors.append("Quantity must be a positive number.")
            except ValueError:
                errors.append("Quantity must be a valid number.")
        else:
            cquantity = None

        if cprice:
            try:
                cprice = float(cprice)
                if cprice <= 0:
                    errors.append("Price must be a positive number.")
            except ValueError:
                errors.append("Price must be a valid number.")
        else:
            cprice = None

        if errors:
            supplier_data = Supplier.objects.all()
            existing_rfq = OrderHasItemSupplier.objects.filter(order_id=order_id)
            order_item = get_object_or_404(OrderHasItem, order_id=order_id)
            item = order_item.item

            context = {
                'errors': errors,
                'data2': supplier_data,
                'existing_rfq': existing_rfq,
                'order_id': order_id,
                'item': item,
            }
            return render(request, 'procurement/rfq_add.html', context)

        order_item = OrderHasItem.objects.get(order_id=order_id)
        order_item_quantity = float(order_item.quantity)

        order_supplier_quantity = OrderHasItemSupplier.objects.filter(order_id=order_id).aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
        total_quantity = order_supplier_quantity + cquantity

        if total_quantity <= order_item_quantity:
            query = OrderHasItemSupplier.objects.create(supplier_id=csupplier_name, item_id=citem_id, order_id=order_id, quantity=cquantity, price=cprice, status='Pending', modified_date=cdate, inventory_status='Pending')
            messages.success(request, "RFQ Added Successfully!")
        else:
            messages.error(request, "Total RFQ quantity exceeds available quantity.")
        
        return redirect(f"/request_order_view/{order_id}")

    supplier_data = Supplier.objects.all()
    existing_rfq = OrderHasItemSupplier.objects.filter(order_id=order_id)

    order_item = get_object_or_404(OrderHasItem, order_id=order_id)
    item = order_item.item
    
    context = {
        'data2': supplier_data,
        'existing_rfq': existing_rfq,
        'order_id': order_id,
        'item': item,
    }

    return render(request, 'procurement/rfq_add.html', context)

@login_required(login_url='login')
def rfq_edit(request,id):
    if not request.user.has_perm('erp.change_orderhasitemsupplier'):
        return HttpResponse('You are not authorised to view this page', status=403)
    edit = get_object_or_404(OrderHasItemSupplier, id=id)
    
    if request.method == "POST":
        csupplier_name=request.POST.get('supplier_name')
        citem_id=request.POST.get('item_id')
        cquantity=request.POST.get('quantity')
        cprice=request.POST.get('price')
        cdate = datetime.now().date()

        errors = []
        if cquantity:
            try:
                cquantity = float(cquantity)
                if cquantity <= 0:
                    errors.append("Quantity must be a positive number.")
            except ValueError:
                errors.append("Quantity must be a valid number.")
        else:
            cquantity = None

        if cprice:
            try:
                cprice = float(cprice)
                if cprice <= 0:
                    errors.append("Price must be a positive number.")
            except ValueError:
                errors.append("Price must be a valid number.")
        else:
            cprice = None

        if errors:
            d = OrderHasItemSupplier.objects.get(id=id)
            order_data = OrderHasItem.objects.filter(order__request_approved='approved').values('item_id').distinct()
            supplier_data = Supplier.objects.all()
            item = get_object_or_404(Item, pk=edit.item_id)  

            context = {
                'data1': order_data,
                'data2': supplier_data,
                'd': d,
                'item': item,
                'errors': errors,
            }

            return render(request, 'procurement/rfq_edit.html', context)
        
        edit.supplier_id = csupplier_name
        edit.item_id = citem_id
        edit.quantity = cquantity
        edit.price = cprice
        edit.modified_date = cdate

        edit.save()
        messages.warning(request, "RFQ Updated Successfully!")
        return redirect(reverse('request_order_view', args=[edit.order_id]))

    d = OrderHasItemSupplier.objects.get(id=id)
    order_data = OrderHasItem.objects.filter(order__request_approved='approved').values('item_id').distinct()
    supplier_data = Supplier.objects.all()
    item = get_object_or_404(Item, item_id=edit.item_id)
    
    context = {
        'data1': order_data,
        'data2' : supplier_data,
        'd': d,
        'item': item,
    }

    return render(request, 'procurement/rfq_edit.html', context)

def rfq_delete(request, id):
    if not request.user.has_perm('erp.delete_orderhasitemsupplier'):
        return HttpResponse('You are not authorised to view this page', status=403)
    d = OrderHasItemSupplier.objects.get(id=id)
    order_id = d.order_id
    d.delete()
    messages.error(request, "RFQ Deleted Successfully!")
    return redirect(reverse('request_order_view', args=[order_id]))

def approve_rfq(request, id):
    try:
        order_item_supplier = OrderHasItemSupplier.objects.get(pk=id)
        order_item_supplier.status = 'Approved'
        order_item_supplier.save()

        return JsonResponse({'message': 'Request for quote approved successfully.'})
    except OrderHasItemSupplier.DoesNotExist:
        return JsonResponse({'error': 'Order has item supplier not found.'}, status=404)
    
def reject_rfq(request, id):
    try:
        with transaction.atomic():
            order_item_supplier = OrderHasItemSupplier.objects.get(pk=id)
            order_item_supplier.status = 'Rejected'
            order_item_supplier.save()
        
        return JsonResponse({'message': 'Request for quote rejected successfully.'})
    except OrderHasItemSupplier.DoesNotExist:
        return JsonResponse({'error': 'Order has item supplier not found.'}, status=404)
    
@login_required(login_url='login')
def add_extra_details(request):
    order_item_id = request.POST.get('order_item_id')
    discount = request.POST.get('discount')
    extra_charges = request.POST.get('extra_charges')
    extra_charge_reason = request.POST.get('extra_charge_reason')
    taxes_in_percent = request.POST.get('taxes_in_percent')

    errors = []
    if not discount:
        discount = 0.0
    try:
        discount = float(discount)
    except ValueError:
        errors.append("Discount must be a valid number.")

    if not extra_charges:
        extra_charges = 0.0
    try:
        extra_charges = float(extra_charges)
    except ValueError:
        errors.append("Extra charges must be a valid number.")

    if not extra_charge_reason:
        extra_charges_reason = None


    if not taxes_in_percent:
        taxes_in_percent = 0.0
    try:
        taxes_in_percent = float(taxes_in_percent)
    except ValueError:
        errors.append("Taxes in percent must be a valid number.")

    if errors:
        for error in errors:
            messages.error(request, error)
        return redirect('/purchase_order') 


    try:
        order_item = OrderHasItem.objects.get(id=order_item_id)
        order_item.discount = discount
        order_item.extra_charges = extra_charges
        order_item.extracharge_reasons = extra_charge_reason
        order_item.taxes_in_percent = taxes_in_percent
        order_item.save()
        messages.success(request, "Extra details added successfully!")
    except OrderHasItem.DoesNotExist:
        messages.error(request, "Order item not found.")

    return redirect('/purchase_order')

@login_required(login_url='login')
def purchase_order(request):
    if not request.user.has_perm('erp.view_orderhasitemsupplier'):
        return HttpResponse('You are not authorised to view this page', status=403)
    approved_supp = OrderHasItemSupplier.objects.filter(status='approved').values('id','supplier_id', 'order_id', 'item_id', 'quantity', 'price', 'status', 'modified_date','inventory_status').distinct()
    item_data = Item.objects.all()
    supplier_data = Supplier.objects.all()
    inventory_data = Order.objects.all()

    paginated_data = paginate_data(request, approved_supp, 10) 
    
    context = {"approved_supp": paginated_data, 'item_data': item_data, 'supplier_data': supplier_data, 'inventory_data': inventory_data}

    return render(request, 'procurement/purchase_order.html', context)

@login_required(login_url='login')
def generate_purchase_order(request, order_id):
    
    data = OrderHasItemSupplier.objects.filter(order_id=order_id, status='approved')
    item_data = Item.objects.all()
    supplier_ids = set(item.supplier.farm_entity_id for item in data)
    current_date = timezone.now()
    contact_data = []
    address_data = []
    supplier_data = Supplier.objects.filter(farm_entity_id__in=supplier_ids)
    
    for supplier_id in supplier_ids:
        unique_contact_types = set()
        distinct_contacts = []
        all_contacts = FarmEntityContact.objects.filter(farm_entity_id=supplier_id)

        for contact in all_contacts:
            if contact.contact_type_id not in unique_contact_types:
                distinct_contacts.append(contact)
                unique_contact_types.add(contact.contact_type_id)

        contact_data.extend(distinct_contacts)

    for supplier_id in supplier_ids:
        address_qs = FarmEntityAddress.objects.filter(farm_entity_id=supplier_id).first()
        if address_qs:
            address_data.append(address_qs)


    farm_data = Farm.objects.all()
    farmcontacts_data = []
    for farm in farm_data:
        all_contacts = FarmContacts.objects.filter(farm_id=farm.id)
        unique_contact_types = set()
        distinct_contacts = []
        
        for contact in all_contacts:
            if contact.contact_type_id not in unique_contact_types:
                distinct_contacts.append(contact)
                unique_contact_types.add(contact.contact_type_id)

        farmcontacts_data.extend(distinct_contacts)
    
    multiplied_values = {}
    total = Decimal(0) 

    total_discount = Decimal(0)
    total_extra_charges = Decimal(0)
    total_tax = Decimal(0)
    
    for item in data:
        order_item = item.order 
        quantity = Decimal(item.quantity)  
        price = Decimal(item.price) 

        discount = Decimal(order_item.discount or 0)
        extra_charges = Decimal(order_item.extra_charges or 0)
        tax = Decimal(order_item.taxes_in_percent or 0)

        multiplied_value = quantity * price
        multiplied_values[item] = multiplied_value  
        total += multiplied_value

        total_discount += discount
        total_extra_charges += extra_charges
        total_tax += (multiplied_value * tax / 100)

    grand_total = total - total_discount + total_extra_charges + total_tax

    context = {
        'data': data,
        'item_data': item_data, 
        'supplier_data': supplier_data,
        'multiplied_values': multiplied_values,
        'total': total, 

        'total_discount': total_discount,
        'total_extra_charges': total_extra_charges,
        'total_tax': total_tax, 
        'grand_total': grand_total,

        'current_date': current_date,
        'contact_data': contact_data,
        'address_data': address_data,
        'farm_data': farm_data,
        'farmcontacts_data': farmcontacts_data,
    }

    return render(request, 'procurement/generate_purchase_order.html', context)

from django.db.models import Q
def approve_inventory(request, id):
    try:
        order_has_item_supplier = get_object_or_404(OrderHasItemSupplier, pk=id)
        order_has_item_supplier.inventory_status = 'Approved'
        order_has_item_supplier.save()

        item = order_has_item_supplier.item
        quantity = float(order_has_item_supplier.quantity)
        current_unit_price = order_has_item_supplier.price
        
        order_id = order_has_item_supplier.order_id 
        order_has_item = get_object_or_404(OrderHasItem, order_id=order_id)
        type = order_has_item.type
        item_measurement = order_has_item.item_measurement

        existing_inventory_item = Stock.objects.filter(
            item=item,
            type=type,
            item_measurement=item_measurement
        ).first()

        print("Existing Inventory Item:", existing_inventory_item)

        if existing_inventory_item:
            existing_inventory_item.quantity = str(float(existing_inventory_item.quantity) + quantity)
            existing_inventory_item.current_unit_price = current_unit_price
            existing_inventory_item.modified_date = timezone.now()
            existing_inventory_item.save()
        else:
            Stock.objects.create(
                item=item,
                quantity=str(quantity),
                current_unit_price=current_unit_price,
                type=type,
                modified_date=timezone.now(),
                item_measurement=item_measurement,
                approval_status='Approved'
            )

        return JsonResponse({'message': 'Inventory approved successfully.'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def reject_inventory(request, id):

    try:
        order_has_item_supplier = get_object_or_404(OrderHasItemSupplier, pk=id)
        order_has_item_supplier.inventory_status = 'Rejected'
        order_has_item_supplier.save()

        return JsonResponse({'message': 'Inventory rejected successfully.'})
    except Exception as e:
        return JsonResponse({'message': 'An error occurred: ' + str(e)}, status=400)


@login_required(login_url='login')
def item_measurement(request):
    if not request.user.has_perm('erp.view_itemmeasurement'):
        return HttpResponse('You are not authorised to view this page', status=403)
    data = ItemMeasurement.objects.all()
    paginated_data = paginate_data(request, data, 10) 
    context = {"data1":paginated_data}

    return render(request, 'inventory/item_measurement.html', context)

@login_required(login_url='login')
def item_measurement_add(request):
    if not request.user.has_perm('erp.add_itemmeasurement'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method=="POST":
        cmeasurement=request.POST.get('measurement')
        cdescription=request.POST.get('description')
        cdate = datetime.now().date()

        query = ItemMeasurement(measurement=cmeasurement, description=cdescription, modified_date=cdate)
        query.save()
        messages.success(request, "Item Measurement Added Successfully!")
        return redirect("/item_measurement")

    return render(request, 'inventory/item_measurement_add.html')

@login_required(login_url='login')
def item_measurement_edit(request,id):
    if not request.user.has_perm('erp.change_itemmeasurement'):
        return HttpResponse('You are not authorised to view this page', status=403)
    edit = ItemMeasurement.objects.get(id=id)
    
    if request.method == "POST":
        cmeasurement=request.POST.get('measurement')
        cdescription=request.POST.get('description')
        cdate = datetime.now().date()
        
        edit.measurement = cmeasurement
        edit.description = cdescription
        edit.modified_date = cdate
        
        edit.save()
        messages.warning(request, "Item Measurement Updated Successfully!")
        return redirect("/item_measurement")

    d = ItemMeasurement.objects.get(id=id)
    context = {"d": d}

    return render(request, 'inventory/item_measurement_edit.html', context)

def item_measurement_delete(request, id):
    if not request.user.has_perm('erp.delete_itemmeasurement'):
        return HttpResponse('You are not authorised to view this page', status=403)
    d = ItemMeasurement.objects.get(id=id)
    d.delete()
    messages.error(request, "Item Measurement Deleted Successfully!")
    return redirect("/item_measurement")


@login_required(login_url='login')
def stock(request):
    if not request.user.has_perm('erp.view_stock'):
        return HttpResponse('You are not authorised to view this page', status=403)
    data = Stock.objects.all()
    paginated_data = paginate_data(request, data, 10) 
    context = {"data1":paginated_data}

    return render(request, 'inventory/stock.html', context)


@login_required(login_url='login')
def stock_add(request):
    if not request.user.has_perm('erp.add_stock'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method=="POST":
        cquantity=request.POST.get('quantity')
        ctype=request.POST.get('type')
        citem_id=request.POST.get('item_id')
        citem_measurement_id=request.POST.get('item_measurement_id')
        cmodified_date = datetime.now().date()

        existing_inventory_item = Stock.objects.filter(
            item_id=citem_id,
            item_measurement_id=citem_measurement_id,
            type=ctype
        ).first()

        if existing_inventory_item:
            existing_inventory_item.quantity = str(float(existing_inventory_item.quantity) + float(cquantity))
            existing_inventory_item.modified_date = cmodified_date
            existing_inventory_item.save()
            messages.success(request, "Stock updated successfully!")
            return redirect("/stock")
        else:
            Stock.objects.create(quantity=cquantity,type_id=ctype,item_id=citem_id,item_measurement_id=citem_measurement_id,modified_date=cmodified_date)
            messages.success(request, "Added to Stock Successfully!")
            return redirect("/stock")
    
    item_data = Item.objects.all()
    measurement_data = ItemMeasurement.objects.all()
    type_data = ItemType.objects.all()
    context = {
        'data1': item_data,
        'data2': measurement_data,
        'data3': type_data,
    }

    return render(request, 'inventory/stock_add.html', context)

@login_required(login_url='login')
def stock_edit(request,stock_id):
    if not request.user.has_perm('erp.change_stock'):
        return HttpResponse('You are not authorised to view this page', status=403)
    edit = Stock.objects.get(stock_id=stock_id)
    
    if request.method == "POST":
        cquantity=request.POST.get('quantity')
        ctype=request.POST.get('type')
        citem_id=request.POST.get('item_id')
        citem_measurement_id=request.POST.get('item_measurement_id')
        cmodified_date = datetime.now().date()
        
        edit.quantity = cquantity
        edit.type_id = ctype
        edit.item_id = citem_id
        edit.item_measurement_id = citem_measurement_id
        edit.modified_date = cmodified_date
        
        edit.save()
        messages.warning(request, "Stock Updated Successfully!")
        return redirect("/stock")

    d = Stock.objects.get(stock_id=stock_id)
    data1 = Item.objects.all()
    data2 = ItemMeasurement.objects.all()
    data3 = ItemType.objects.all()
        
    context = {"d": d, "item": edit, "data1": data1, "data2": data2, "data3": data3,}

    return render(request, 'inventory/stock_edit.html', context)

def stock_delete(request, stock_id):
    if not request.user.has_perm('erp.delete_stock'):
        return HttpResponse('You are not authorised to view this page', status=403)
    d = Stock.objects.get(stock_id=stock_id)
    d.delete()
    messages.error(request, "Stock Deleted Successfully!")
    return redirect("/stock")


@login_required(login_url='login')
def stock_in(request):
    if not request.user.has_perm('erp.view_directlyaddeditem'):
        return HttpResponse('You are not authorised to view this page', status=403)
    data = DirectlyAddedItem.objects.all()
    paginated_data = paginate_data(request, data, 10) 
    context = {"data1":paginated_data}

    return render(request, 'inventory/stock_in.html', context)


@login_required(login_url='login')
def stockin_add(request):
    if not request.user.has_perm('erp.add_directlyaddeditem'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method=="POST":
        cquantity=request.POST.get('quantity')
        ctype=request.POST.get('type')
        citem_id=request.POST.get('item_id')
        citem_measurement_id=request.POST.get('item_measurement_id')
        cunit_price = request.POST.get('unit_price')
        cdescription = request.POST.get('description')
        cquantity = float(cquantity)
        cunit_price = float(cunit_price)
        ctotal_price = cunit_price * cquantity
        capproval_status = 'Pending'

        errors = []
        if cquantity:
            try:
                cquantity = float(cquantity)
                if cquantity <= 0:
                    errors.append("Quantity must be a positive number.")
            except ValueError:
                errors.append("Quantity must be a valid number.")
        else:
            cquantity = None

        if cunit_price:
            try:
                cunit_price = float(cunit_price)
                if cunit_price <= 0:
                    errors.append("Price must be a positive number.")
            except ValueError:
                errors.append("Price must be a valid number.")
        else:
            cunit_price = None

        if errors:
            context = {
                'errors': errors,
                'data1': Item.objects.all(),
                'data2': ItemMeasurement.objects.all(),
                'data3': ItemType.objects.all(),
            }
            return render(request, 'inventory/stockin_add.html', context)

        DirectlyAddedItem.objects.create(quantity=cquantity,item_type_id=ctype,item_id=citem_id,measurement_id=citem_measurement_id,unit_price=cunit_price,description=cdescription,total_price=ctotal_price,approval_status=capproval_status)
        messages.success(request, "Stock request sent Successfully!")
        return redirect("/stock_in")
    
    item_data = Item.objects.all()
    measurement_data = ItemMeasurement.objects.all()
    type_data = ItemType.objects.all()
    context = {
        'data1': item_data,
        'data2': measurement_data,
        'data3': type_data,
    }

    return render(request, 'inventory/stockin_add.html', context)

@login_required(login_url='login')
def stockin_edit(request,id):
    if not request.user.has_perm('erp.change_directlyaddeditem'):
        return HttpResponse('You are not authorised to view this page', status=403)
    edit = DirectlyAddedItem.objects.get(id=id)
    
    if request.method == "POST":
        cquantity=request.POST.get('quantity')
        ctype=request.POST.get('type')
        citem_id=request.POST.get('item_id')
        citem_measurement_id=request.POST.get('item_measurement_id')
        cunit_price = request.POST.get('unit_price')
        cdescription = request.POST.get('description')
        cquantity = float(cquantity)
        cunit_price = float(cunit_price)
        ctotal_price = cunit_price * cquantity
        capproval_status = 'Pending'

        errors = []
        if cquantity:
            try:
                cquantity = float(cquantity)
                if cquantity <= 0:
                    errors.append("Quantity must be a positive number.")
            except ValueError:
                errors.append("Quantity must be a valid number.")
        else:
            cquantity = None

        if cunit_price:
            try:
                cunit_price = float(cunit_price)
                if cunit_price <= 0:
                    errors.append("Price must be a positive number.")
            except ValueError:
                errors.append("Price must be a valid number.")
        else:
            cunit_price = None

        if errors:
            context = {
                'errors': errors,
                "d": DirectlyAddedItem.objects.get(id=id), 
                "item": edit, 
                'data1': Item.objects.all(),
                'data2': ItemMeasurement.objects.all(),
                'data3': ItemType.objects.all(),
            }
            return render(request, 'inventory/stockin_edit.html', context)
        
        edit.quantity = cquantity
        edit.item_type_id = ctype
        edit.item_id = citem_id
        edit.measurement_id = citem_measurement_id
        edit.unit_price = cunit_price
        edit.description = cdescription
        edit.total_price = ctotal_price
        edit.approval_status = capproval_status
        
        edit.save()
        messages.warning(request, "Stock request updated Successfully!")
        return redirect("/stock_in")

    d = DirectlyAddedItem.objects.get(id=id)
    data1 = Item.objects.all()
    data2 = ItemMeasurement.objects.all()
    data3 = ItemType.objects.all()
        
    context = {"d": d, "item": edit, "data1": data1, "data2": data2, "data3": data3,}

    return render(request, 'inventory/stockin_edit.html', context)

def stockin_delete(request, id):
    if not request.user.has_perm('erp.delete_directlyaddeditem'):
        return HttpResponse('You are not authorised to view this page', status=403)
    d = DirectlyAddedItem.objects.get(id=id)
    d.delete()
    messages.error(request, "Stock request Deleted Successfully!")
    return redirect("/stock_in")


def approve_stockin(request, id):
    try:
        inventory = get_object_or_404(DirectlyAddedItem, pk=id)
        inventory.approval_status = 'Approved'
        inventory.save()

        item = inventory.item
        quantity = float(inventory.quantity)
        current_unit_price = inventory.unit_price
        item_type = inventory.item_type
        item_measurement = inventory.measurement

        existing_inventory_item = Stock.objects.filter(
            item=item,
            type=item_type,
            item_measurement=item_measurement
        ).first()

        if existing_inventory_item:
            existing_inventory_item.quantity = str(float(existing_inventory_item.quantity) + quantity)
            existing_inventory_item.current_unit_price = current_unit_price
            existing_inventory_item.modified_date = timezone.now()
            existing_inventory_item.save()
        else:
            Stock.objects.create(
                item=item,
                quantity=str(quantity),
                current_unit_price=current_unit_price,
                type=item_type,
                modified_date=timezone.now(),
                item_measurement=item_measurement,
                approval_status='Approved'
            )

        return JsonResponse({'message': 'Inventory approved successfully.'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def reject_stockin(request, id):
    try:
        inventory = get_object_or_404(DirectlyAddedItem, pk=id)
        inventory.approval_status = 'Rejected'
        inventory.save()

        return JsonResponse({'message': 'Inventory rejected successfully.'})
    except Exception as e:
        return JsonResponse({'message': 'An error occurred: ' + str(e)}, status=400)


@login_required(login_url='login')
def stock_out(request):
    if not request.user.has_perm('erp.view_stockout'):
        return HttpResponse('You are not authorised to view this page', status=403)
    data = Stockout.objects.all()
    paginated_data = paginate_data(request, data, 10) 
    context = {"data1":paginated_data}

    return render(request, 'inventory/stock_out.html', context)


@login_required(login_url='login')
def stockout_add(request):
    if not request.user.has_perm('erp.add_stockout'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method=="POST":
        cquantity=request.POST.get('quantity')
        citem_type=request.POST.get('item_type')
        citem_id=request.POST.get('item_name')
        citem_measurement_id=request.POST.get('item_measurement_id')
        cstatus = 'Pending'
        cmodified_date = datetime.now().date()

        errors = []
        if cquantity:
            try:
                cquantity = float(cquantity)
                if cquantity <= 0:
                    errors.append("Quantity must be a positive number.")
            except ValueError:
                errors.append("Quantity must be a valid number.")
        else:
            cquantity = None

        if errors:
            context = {
                'errors': errors,
                'data1': Stock.objects.values('item_id', 'item__name').distinct(),
                'data2': ItemMeasurement.objects.all(),
                'data3': ItemType.objects.all(),
            }
            return render(request, 'inventory/stockout_add.html', context)

        stock_item = Stock.objects.filter(
            item_id=citem_id,
            type_id=citem_type,
            item_measurement_id=citem_measurement_id
        ).first()
        
        if not stock_item:
            errors.append("Stock item not found.")
            context = {
                'errors': errors,
                'data1': Stock.objects.values('item_id', 'item__name').distinct(),
                'data2': ItemMeasurement.objects.all(),
                'data3': ItemType.objects.all(),
            }
            return render(request, 'inventory/stockout_add.html', context)
        
        current_stock_quantity = float(stock_item.quantity)

        if cquantity > current_stock_quantity:
            errors.append("Requested quantity exceeds current stock")
            
            item_data = Stock.objects.values('item_id', 'item__name').distinct()
            measurement_data = ItemMeasurement.objects.all()
            type_data = ItemType.objects.all()
            
            context = {
                'errors': errors,
                'data1': item_data,
                'data2': measurement_data,
                'data3': type_data,
            }
            return render(request, 'inventory/stockout_add.html', context)


        user_profile = UserProfile.objects.get(user=request.user)
        crequested_by_id = user_profile.employee_id

        Stockout.objects.create(quantity=cquantity,item_type_id=citem_type,item_id=citem_id,measurement_id=citem_measurement_id,status=cstatus,modified_date=cmodified_date,requested_by_id=crequested_by_id)
        messages.success(request, "Stock out request sent Successfully!")
        return redirect("/stock_out")
    
    item_data = Stock.objects.values('item_id', 'item__name').distinct()
    measurement_data = ItemMeasurement.objects.all()
    type_data = ItemType.objects.all()
    context = {
        'data1': item_data,
        'data2': measurement_data,
        'data3': type_data,
    }

    return render(request, 'inventory/stockout_add.html', context)

@login_required(login_url='login')
def stockout_edit(request,id):
    if not request.user.has_perm('erp.change_stockout'):
        return HttpResponse('You are not authorised to view this page', status=403)
    edit = Stockout.objects.get(id=id)

    current_item_id = edit.item_id if edit.item_id else None
    current_item_type_id = edit.item_type_id if edit.item_type_id else None
    current_item_measurement_id = edit.measurement_id if edit.measurement_id else None
    
    if request.method == "POST":
        cquantity=request.POST.get('quantity')
        ctype=request.POST.get('item_type')
        citem_id=request.POST.get('item_name')
        citem_measurement_id=request.POST.get('item_measurement_id')
        cstatus = 'Pending'
        cmodified_date = datetime.now().date()

        errors = []
        if cquantity:
            try:
                cquantity = float(cquantity)
                if cquantity <= 0:
                    errors.append("Quantity must be a positive number.")
            except ValueError:
                errors.append("Quantity must be a valid number.")
        else:
            cquantity = None

        if errors:
            context = {
                'errors': errors,
                "d": Stockout.objects.get(id=id), 
                "item": edit,
                'data1': Stock.objects.values('item_id', 'item__name').distinct(),
                'current_item_id': current_item_id,
                'current_item_type_id': current_item_type_id,
                'current_item_measurement_id': current_item_measurement_id,
            }
            return render(request, 'inventory/stockout_edit.html', context)


        stock_item = Stock.objects.filter(
            item_id=citem_id,
            type_id=ctype,
            item_measurement_id=citem_measurement_id
        ).first()
        if not stock_item:
            errors.append("Stock item not found.")
            context = {
                'errors': errors,
                "d": Stockout.objects.get(id=id), 
                "item": edit,
                'data1': Stock.objects.values('item_id', 'item__name').distinct(),
                'current_item_id': current_item_id,
                'current_item_type_id': current_item_type_id,
                'current_item_measurement_id': current_item_measurement_id,

            }
            return render(request, 'inventory/stockout_edit.html', context)
        
        current_stock_quantity = float(stock_item.quantity)

        if cquantity > current_stock_quantity:
            errors.append("Requested quantity exceeds current stock")
            
            d = Stockout.objects.get(id=id)
            data1 = Stock.objects.values('item_id', 'item__name').distinct()
            
            context = {
                'errors': errors,
                'd': d,
                'item': edit,
                'data1': data1,
                'current_item_id': current_item_id,
                'current_item_type_id': current_item_type_id,
                'current_item_measurement_id': current_item_measurement_id,
            }
            return render(request, 'inventory/stockout_edit.html', context)
        
        edit.quantity = cquantity
        edit.item_type_id = ctype
        edit.item_id = citem_id
        edit.measurement_id = citem_measurement_id
        edit.status = cstatus
        edit.modified_date = cmodified_date
        
        edit.save()
        messages.warning(request, "Stockout Updated Successfully!")
        return redirect("/stock_out")

    d = Stockout.objects.get(id=id)
    data1 = Stock.objects.values('item_id', 'item__name').distinct()
        
    context = {
        'd': d,
        'item': edit,
        'data1': data1,
        'current_item_id': current_item_id,
        'current_item_type_id': current_item_type_id,
        'current_item_measurement_id': current_item_measurement_id,
    }

    return render(request, 'inventory/stockout_edit.html', context)

def stockout_delete(request, id):
    if not request.user.has_perm('erp.delete_stockout'):
        return HttpResponse('You are not authorised to view this page', status=403)
    d = Stockout.objects.get(id=id)
    d.delete()
    messages.error(request, "Stockout Deleted Successfully!")
    return redirect("/stock_out")

    
def approve_stockout(request, id):
    try:
        inventory = get_object_or_404(Stockout, pk=id)
        stock_item = Stock.objects.filter(
            item=inventory.item,
            type=inventory.item_type,
            item_measurement=inventory.measurement
        ).first()
        
        if not stock_item:
            return JsonResponse({'error': 'Stock item not found'}, status=404)
        
        current_stock_quantity = float(stock_item.quantity)
        requested_quantity = float(inventory.quantity)
        
        if requested_quantity > current_stock_quantity:
            return JsonResponse({'error': 'Requested quantity exceeds current stock'}, status=400)
        
        user_profile = UserProfile.objects.get(user=request.user)
        inventory.approved_by_id = user_profile.employee_id
        inventory.status = 'Approved'
        inventory.save()

        new_stock_quantity = current_stock_quantity - requested_quantity
        stock_item.quantity = str(new_stock_quantity)
        stock_item.modified_date = timezone.now()
        stock_item.save()

        if new_stock_quantity == 0:
            stock_item.delete()
        else:
            stock_item.save()
        
        return JsonResponse({'message': 'Inventory approved and stock updated successfully.'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def reject_stockout(request, id):
    try:
        inventory = get_object_or_404(Stockout, pk=id)
        user_profile = UserProfile.objects.get(user=request.user)
        inventory.approved_by_id = user_profile.employee_id
        inventory.status = 'Rejected'
        inventory.save()

        return JsonResponse({'message': 'Inventory rejected successfully.'})
    except Exception as e:
        return JsonResponse({'message': 'An error occurred: ' + str(e)}, status=400)




@login_required(login_url='login')
def department(request):
    if not request.user.has_perm('erp.view_department'):
        return HttpResponse('You are not authorised to view this page', status=403)
    data = Department.objects.all()
    paginated_data = paginate_data(request, data, 10) 
    context = {"data1":paginated_data}

    return render(request, 'employee/department.html', context)

@login_required(login_url='login')
def department_add(request):
    if not request.user.has_perm('erp.add_department'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method=="POST":
        cdepartment=request.POST.get('department')
        cmanager_id=request.POST.get('manager_id')

        query = Department(department_name=cdepartment, manager_id=cmanager_id)
        query.save()
        messages.success(request, "Department Added Successfully!")
        return redirect("/department")

    data1 = Employee.objects.all()
    context = {"data1":data1}

    return render(request, 'employee/department_add.html', context)

@login_required(login_url='login')
def department_edit(request,department_id):
    if not request.user.has_perm('erp.change_department'):
        return HttpResponse('You are not authorised to view this page', status=403)
    edit = Department.objects.get(department_id=department_id)
    
    if request.method == "POST":
        cdepartment=request.POST.get('department')
        cmanager_id=request.POST.get('manager_id')

        edit.department_name = cdepartment
        edit.manager_id = cmanager_id
        edit.save()
        messages.warning(request, "Department Updated Successfully!")
        return redirect("/department")

    d = Department.objects.get(department_id=department_id)
    data1 = Employee.objects.all()
    context = {"d": d, "data1":data1}

    return render(request, 'employee/department_edit.html', context)

def department_delete(request, department_id):
    if not request.user.has_perm('erp.delete_department'):
        return HttpResponse('You are not authorised to view this page', status=403)
    d = Department.objects.get(department_id=department_id)
    d.delete()
    messages.error(request, "Department Deleted Successfully!")
    return redirect("/department")

@login_required(login_url='login')
def employee(request):
    if not request.user.has_perm('erp.view_employee'):
        return HttpResponse('You are not authorised to view this page', status=403)
    data = Employee.objects.all()
    paginated_data = paginate_data(request, data, 10) 
    context = {"data1":paginated_data}

    return render(request, 'employee/employee.html', context)

@login_required(login_url='login')
def employee_view(request, farm_entity_id):
    if not request.user.has_perm('erp.view_employee'):
        return HttpResponse('You are not authorised to view this page', status=403)

    farm_entity = get_object_or_404(FarmEntity, pk=farm_entity_id)
    person = get_object_or_404(Person, farm_entity=farm_entity)
    employee = get_object_or_404(Employee, person_farm_entity=person)
    experience = EmployeeExperience.objects.filter(person_farm_entity=employee)
    contact = FarmEntityContact.objects.filter(farm_entity=farm_entity)
    address = FarmEntityAddress.objects.filter(farm_entity=farm_entity)
    guarantee = Guarantee.objects.filter(person_farm_entity=employee)
    jobhistory = JobHistory.objects.filter(person_farm_entity=employee)

    context = {
        'person': person,
        'employee': employee,
        'farm_entity_id': farm_entity_id, 
        'experience': experience,
        'contact': contact,
        'address': address,
        'jobhistory': jobhistory,
        'guarantee': guarantee,
    }

    return render(request, 'employee/employee_view.html', context)

@login_required(login_url='login')
def employee_add(request):
    if not request.user.has_perm('erp.add_employee'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method == "POST":
        ctitle = request.POST.get('title')
        ctype = request.POST.get('type')
        cfname = request.POST.get('fname')
        cmname = request.POST.get('mname')
        clname = request.POST.get('lname')
        cdob = request.POST.get('dob')
        cmarital_status = request.POST.get('marital_status')
        cgender = request.POST.get('gender')
        cdepartment = request.POST.get('department')
        csalary = request.POST.get('salary')
        chire_data = request.POST.get('hire_date')
        cavailableleavehours = 384
        cnational_id = request.POST.get('national_id')
        ccontract_type = request.POST.get('contract_type')
        ccontract_period = request.POST.get('contract_period')
        cjob = request.POST.get('job')
        cdate = datetime.now().date()
        cstatus = "Active"

        errors = []
        if cdob:
            parsed_dob = parse_date(cdob)
            if not parsed_dob:
                errors.append('Date of Birth must be in YYYY-MM-DD format.')
            else:
                cdob = parsed_dob
        else:
            cdob = None 

        if chire_data:
            parsed_hire_data = parse_date(chire_data)
            if not parsed_hire_data:
                errors.append('Hire date must be in YYYY-MM-DD format.')
            else:
                chire_data = parsed_hire_data
        else:
            chire_data = None 

        if not cgender:
            errors.append('Gender is required.')

        if csalary:
            try:
                csalary = float(csalary)
                if csalary <= 0:
                    errors.append("Salary must be a positive number.")
            except ValueError:
                errors.append('Salary must be a number.')
        else:
            csalary = None 

        if ccontract_period:
            try:
                ccontract_period = float(ccontract_period)
            except ValueError:
                errors.append('Contract Period must be a number.')
        else:
            ccontract_period = None 

        
        if errors:
            context = {
                'errors': errors,
                'data2': PersonTitle.objects.all(),
                'data3': PersonType.objects.all(),
                'data1': Person.objects.all(),
                'data4': Job.objects.all(),
                'data5': Department.objects.all(),
                'data6': ContactType.objects.all(),
                'data7': Region.objects.all(),
                'data8': Employee.objects.all(),
                'data9': GuaranteeType.objects.all() 
            }
            return render(request, 'employee/employee_add.html', context)

        farm_entity = FarmEntity.objects.create(modified_date=timezone.now())

        person = Person.objects.create(
            farm_entity=farm_entity,
            person_title_id=ctitle,
            person_type_id=ctype,
            first_name=cfname,
            middle_name=cmname,
            last_name=clname,
            date_of_birth=cdob,
            marital_status=cmarital_status,
            gender=cgender
        )

        employee = Employee.objects.create(
            person_farm_entity=person,
            salary=csalary,
            hire_date=chire_data,
            available_leave_hours=cavailableleavehours,
            national_id=cnational_id,
            contract_type=ccontract_type,
            contract_period_in_month=ccontract_period,
            job_id=cjob,
            department_id=cdepartment,
            modified_date=cdate,
            status=cstatus,
        )

        messages.success(request, "Employee Added Successfully!")
        return redirect("/employee")

    title_data = PersonTitle.objects.all()
    type_data = PersonType.objects.all()
    person_data = Person.objects.all()
    job_data = Job.objects.all()
    dep_data = Department.objects.all()
    contact_data = ContactType.objects.all() 
    region_data = Region.objects.all() 
    employee_data = Employee.objects.all() 
    guarantee_data = GuaranteeType.objects.all() 

    context = {
        'data1': person_data,
        'data2': title_data,
        'data3': type_data,
        'data4': job_data,
        'data5': dep_data,
        'data6': contact_data, 
        'data7': region_data,   
        'data8': employee_data,  
        'data9': guarantee_data,  
    }

    return render(request, 'employee/employee_add.html', context)

@login_required(login_url='login')
def employee_edit(request, farm_entity_id):
    if not request.user.has_perm('erp.change_employee'):
        return HttpResponse('You are not authorised to view this page', status=403)
    farm_entity = get_object_or_404(FarmEntity, pk=farm_entity_id)
    person = get_object_or_404(Person, farm_entity=farm_entity)
    employee = get_object_or_404(Employee, person_farm_entity=person)

    if request.method == "POST":
        person.person_title_id = request.POST.get('title')
        person.person_type_id = request.POST.get('type')
        person.first_name = request.POST.get('fname')
        person.middle_name = request.POST.get('mname')
        person.last_name = request.POST.get('lname')
        person.date_of_birth = request.POST.get('dob')
        person.marital_status = request.POST.get('marital_status')
        person.gender = request.POST.get('gender')

        employee.department_id = request.POST.get('department')
        employee.salary = request.POST.get('salary')
        employee.hire_date = request.POST.get('hire_date')
        employee.national_id = request.POST.get('national_id')
        employee.contract_type = request.POST.get('contract_type')
        employee.contract_period_in_month = request.POST.get('contract_period')
        employee.job_id = request.POST.get('job')

        errors = []
        if person.date_of_birth:
            parsed_dob = parse_date(person.date_of_birth)
            if not parsed_dob:
                errors.append('Date of Birth must be in YYYY-MM-DD format.')
            else:
                person.date_of_birth = parsed_dob
        else:
            person.date_of_birth = None 

        if employee.hire_date:
            parsed_hire_data = parse_date(employee.hire_date)
            if not parsed_hire_data:
                errors.append('Hire date must be in YYYY-MM-DD format.')
            else:
                employee.hire_date = parsed_hire_data
        else:
            employee.hire_date = None 

        if not person.gender:
            errors.append('Gender is required.')

        if employee.salary:
            try:
                employee.salary = float(employee.salary)
                if employee.salary <= 0:
                    errors.append("Salary must be a positive number.")
            except ValueError:
                errors.append('Salary must be a number.')
        else:
            employee.salary = None 

        if employee.contract_period_in_month:
            try:
                employee.contract_period_in_month = float(employee.contract_period_in_month)
            except ValueError:
                errors.append('Contract Period must be a number.')
        else:
            employee.contract_period_in_month = None

        if errors:
            context = {
                'errors': errors,
                'data2': PersonTitle.objects.all(),
                'data3': PersonType.objects.all(),
                'data4': Job.objects.all(),
                'data5': Department.objects.all(),
                'data6': ContactType.objects.all(),
                'data7': Region.objects.all(),
                'data9': GuaranteeType.objects.all(),
                'farm_entity_id': farm_entity_id,
                'person': person,  
                'employee': employee,  
            }
            return render(request, 'employee/employee_edit.html', context)

        person.save()
        employee.save()

        messages.warning(request, "Employee Updated Successfully!")
        return redirect("/employee")

    title_data = PersonTitle.objects.all()
    type_data = PersonType.objects.all()
    job_data = Job.objects.all()
    dep_data = Department.objects.all()

    contact_data = ContactType.objects.all() 
    region_data = Region.objects.all() 
    employee_data = Employee.objects.all() 
    guarantee_data = GuaranteeType.objects.all() 

    context = {
        'data2': title_data,
        'data3': type_data,
        'data4': job_data,
        'data5': dep_data,
        'person': person,
        'employee': employee,
        'farm_entity_id': farm_entity_id, 
        
        'data6': contact_data, 
        'data7': region_data,   
        'data8': employee_data,  
        'data9': guarantee_data,  

    }

    return render(request, 'employee/employee_edit.html', context)


def employee_delete(request, farm_entity_id):
    if not request.user.has_perm('erp.delete_employee'):
        return HttpResponse('You are not authorised to view this page', status=403)
    farm_entity = get_object_or_404(FarmEntity, farm_entity_id=farm_entity_id)

    person = get_object_or_404(Person, farm_entity=farm_entity)
    employee = get_object_or_404(Employee, person_farm_entity=person)
    person.delete()
    employee.delete()

    farm_entity.delete()

    messages.error(request, "Employee deleted successfully!")
    
    return redirect("/employee")

@login_required(login_url='login')
def add_contact(request):
    if not request.user.has_perm('erp.add_farmentitycontact'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method == 'POST':
        cemployee_id = request.POST.get('employee_id')
        ccontact_type = request.POST.get('contact_type')
        ccontact = request.POST.get('contact')
            
        contact = FarmEntityContact(
            farm_entity_id=cemployee_id,
            contact_type_id=ccontact_type,
            contact=ccontact
        )
        contact.save()

        messages.success(request, "Employee Contact Added Successfully!")
        return redirect("/employee")

    return render(request, 'employee/employee_edit.html')

@login_required(login_url='login')
def add_address(request):
    if not request.user.has_perm('erp.add_farmentityaddress'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method == 'POST':
        cemployee_id = request.POST.get('employee_id')
        cregion = request.POST.get('region')
        ccountry = request.POST.get('country')
        czone_subcity = request.POST.get('zone_subcity')
        cworeda = request.POST.get('woreda')
        ckebele = request.POST.get('kebele')
        chouse_no = request.POST.get('house_no')
        cstreet = request.POST.get('street')
            
        address = FarmEntityAddress(
            farm_entity_id=cemployee_id,
            region_id=cregion,
            country=ccountry,
            zone_subcity=czone_subcity,
            woreda=cworeda,
            kebele=ckebele,
            house_number=chouse_no,
            street_name=cstreet,
        )
        address.save()

        messages.success(request, "Employee Address Added Successfully!")
        return redirect("/employee")

    return render(request, 'employee/employee_edit.html')

@login_required(login_url='login')
def add_experience(request):
    if not request.user.has_perm('erp.add_employeeexperience'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method == 'POST':
        cemployee_id = request.POST.get('employee_id')
        ccompany = request.POST.get('company')
        ctitle = request.POST.get('title')
        cstart_date = request.POST.get('start_date')
        cend_date = request.POST.get('end_date')
        csalary = request.POST.get('salary')

        errors = []
        if cstart_date:
            parsed_start_date = parse_date(cstart_date)
            if not parsed_start_date:
                errors.append('Start date must be in YYYY-MM-DD format.')
            else:
                cstart_date = parsed_start_date
        else:
            cstart_date = None 
            
        if cend_date:
            parsed_end_date = parse_date(cend_date)
            if not parsed_end_date:
                errors.append('End date must be in YYYY-MM-DD format.')
            else:
                cend_date = parsed_end_date
        else:
            cend_date = None 

        if csalary:
            try:
                csalary = float(csalary)
                if csalary <= 0:
                    errors.append("Salary must be a positive number.")
            except ValueError:
                errors.append('Salary must be a number.')
        else:
            csalary = None 

        if errors:
            context = {
                'errors': errors,
            }
            return render(request, 'employee/employee_edit.html', context)
            

        experience = EmployeeExperience(
            person_farm_entity_id=cemployee_id,
            company=ccompany,
            title=ctitle,
            start_date=cstart_date,
            end_date=cend_date,
            salary=csalary,
        )
        experience.save()

        messages.success(request, "Employee Experience Added Successfully!")
        return redirect("/employee")

    return render(request, 'employee/employee_edit.html')

@login_required(login_url='login')
def add_guarantee(request):
    if not request.user.has_perm('erp.add_guarantee'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method == 'POST':
        cemployee_id = request.POST.get('employee_id')
        cguarantee_type = request.POST.get('guarantee_type')
        cname = request.POST.get('name')
        csalary_evaluation = request.POST.get('salary_evaluation')

        farm_entity = FarmEntity.objects.create(modified_date=timezone.now())

        errors = []
        if csalary_evaluation:
            try:
                csalary_evaluation = float(csalary_evaluation)
                if csalary_evaluation <= 0:
                    errors.append("Salary must be a positive number.")
            except ValueError:
                errors.append('Salary must be a number.')
        else:
            csalary_evaluation = None 

        if errors:
            context = {
                'errors': errors,
            }
            return render(request, 'employee/employee_edit.html', context)
            
        guarantee = Guarantee(
            farm_entity=farm_entity,
            person_farm_entity_id=cemployee_id,
            guarantee_type_id=cguarantee_type,
            name=cname,
            salary_evaluation=csalary_evaluation,
        )
        guarantee.save()

        messages.success(request, "Employee Guarantee Added Successfully!")
        return redirect("/employee")

    return render(request, 'employee/employee_edit.html')

@login_required(login_url='login')
def add_jobhistory(request):
    if not request.user.has_perm('erp.add_jobhistory'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method == 'POST':
        cemployee_id = request.POST.get('employee_id')
        cjob_id = request.POST.get('job_id')
        cdepartment_id = request.POST.get('department_id')
        cstart_date = request.POST.get('start_date')
        cend_date = request.POST.get('end_date')
        csalary = request.POST.get('salary')
        cpromotion_or_demotion = request.POST.get('promotion_or_demotion')

        errors = []
        if csalary:
            try:
                csalary = float(csalary)
                if csalary <= 0:
                    errors.append("Salary must be a positive number.")
            except ValueError:
                errors.append('Salary must be a number.')
        else:
            csalary = None 

        if cstart_date:
            parsed_start_date = parse_date(cstart_date)
            if not parsed_start_date:
                errors.append('Start date must be in YYYY-MM-DD format.')
            else:
                cstart_date = parsed_start_date
        else:
            cstart_date = None 
            
        if cend_date:
            parsed_end_date = parse_date(cend_date)
            if not parsed_end_date:
                errors.append('End date must be in YYYY-MM-DD format.')
            else:
                cend_date = parsed_end_date
        else:
            cend_date = None 

        if errors:
            context = {
                'errors': errors,
            }
            return render(request, 'employee/employee_edit.html', context)

        jobhistory = JobHistory(
            person_farm_entity_id=cemployee_id,
            job_id=cjob_id,
            department_id=cdepartment_id,
            start_date=cstart_date,
            end_date=cend_date,
            salary=csalary,
            promotion_or_demotion=cpromotion_or_demotion,
        )
        jobhistory.save()

        messages.success(request, "Employee Job History Added Successfully!")
        return redirect("/employee")

    return render(request, 'employee/employee_edit.html')

@login_required(login_url='login')
def leave(request):
    if not request.user.has_perm('erp.view_employeeleave'):
        return HttpResponse('You are not authorised to view this page', status=403)
    
    user = request.user
    if not request.user.has_perm('erp.add_employeeleave'):
        data = EmployeeLeave.objects.all()
    else:
        user_profile = get_object_or_404(UserProfile, user=user)
        requester_person = user_profile.employee
        data = EmployeeLeave.objects.filter(person_farm_entity_id=requester_person)

    paginated_data = paginate_data(request, data, 10) 
    context = {"data1":paginated_data}

    return render(request, 'employee/leave.html', context)

@login_required(login_url='login')
def leave_view(request, leave_id):
    if not request.user.has_perm('erp.view_employeeleave'):
        return HttpResponse('You are not authorised to view this page', status=403)
    leave = get_object_or_404(EmployeeLeave, leave_id=leave_id)
    context = {"leave":leave}

    return render(request, 'employee/leave_view.html', context)


@login_required(login_url='login')
def leave_add(request):
    if not request.user.has_perm('erp.add_employeeleave'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method=="POST":
        cstart_date=request.POST.get('start_date')
        cend_date=request.POST.get('end_date')
        creason=request.POST.get('reason')
        capproval_status='Pending'

        user_profile = UserProfile.objects.get(user=request.user)
        cperson_farm_entity_id = user_profile.employee_id

        query = EmployeeLeave.objects.create(start_date=cstart_date, end_date=cend_date, reason=creason,approval_status=capproval_status, person_farm_entity_id=cperson_farm_entity_id)
        query.save()
        messages.success(request, "Leave Request Added Successfully!")
        return redirect("/leave")

    return render(request, 'employee/leave_add.html')

@login_required(login_url='login')
def leave_edit(request,leave_id):
    if not request.user.has_perm('erp.change_employeeleave'):
        return HttpResponse('You are not authorised to view this page', status=403)
    edit = EmployeeLeave.objects.get(leave_id=leave_id)
    
    if request.method == "POST":
        cstart_date=request.POST.get('start_date')
        cend_date=request.POST.get('end_date')
        creason=request.POST.get('reason')
        
        edit.start_date = cstart_date
        edit.end_date = cend_date
        edit.reason = creason
        
        edit.save()
        messages.warning(request, "Request Updated Successfully!")
        return redirect("/leave")

    d = EmployeeLeave.objects.get(leave_id=leave_id)
    context = {"d": d,}

    return render(request, 'employee/leave_edit.html', context)

def leave_delete(request, leave_id):
    if not request.user.has_perm('erp.delete_employeeleave'):
        return HttpResponse('You are not authorised to view this page', status=403)
    d = EmployeeLeave.objects.get(leave_id=leave_id)
    d.delete()
    messages.error(request, "Request Deleted Successfully!")
    return redirect("/leave")

def approve_leave(request, leave_id):
    try:
        leave = EmployeeLeave.objects.get(pk=leave_id)
    
        start_date = leave.start_date
        end_date = leave.end_date
        leave_duration = (end_date - start_date).total_seconds() / 3600 
        
        employee = leave.person_farm_entity
        if employee.available_leave_hours is not None:
            employee.available_leave_hours -= leave_duration
            employee.save()

        user_profile = UserProfile.objects.get(user=request.user)
        leave.approved_by_farm_entity_id = user_profile.employee_id
        leave.approval_status = 'Approved'
        leave.save()
        
        return JsonResponse({'message': 'Leave request approved successfully.'})
    except EmployeeLeave.DoesNotExist:
        return JsonResponse({'error': 'Leave not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def reject_leave(request, leave_id):
    try:
        leave = EmployeeLeave.objects.get(pk=leave_id)
        user_profile = UserProfile.objects.get(user=request.user)
        leave.approved_by_farm_entity_id = user_profile.employee_id
        leave.approval_status = 'Rejected'
        leave.save()
        return JsonResponse({'message': 'Leave request Rejected successfully.'})
    except EmployeeLeave.DoesNotExist:
        return JsonResponse({'error': 'Leave not found.'}, status=404)

@login_required(login_url='login')
def transaction(request):
    if not request.user.has_perm('erp.view_transaction'):
        return HttpResponse('You are not authorised to view this page', status=403)
    data = OtherIncomeExpense.objects.all()
    paginated_data = paginate_data(request, data, 10) 
    context = {"data":paginated_data}

    return render(request, 'finance/transaction.html', context)

@login_required(login_url='login')
def transaction_add(request):
    if not request.user.has_perm('erp.add_transaction'):
        return HttpResponse('You are not authorised to view this page', status=403)
    if request.method=="POST":
        ctransaction_type=request.POST.get('transaction_type')
        ctransaction_date=request.POST.get('transaction_date')
        camount=request.POST.get('amount')
        ctransaction_status=request.POST.get('transaction_status')
        creason=request.POST.get('reason')
        cmodified_date=datetime.now().date()

        errors = []
        if not ctransaction_type:
            errors.append('Transaction Type is required.')
        
        if not ctransaction_status:
            errors.append('Transaction Status is required.')

        if camount:
            try:
                camount = float(camount)
                if camount <= 0:
                    errors.append("Amount must be a positive number.")
            except ValueError:
                errors.append('Amount must be a number.')
        else:
            camount = None 

        if ctransaction_date:
            try:
                ctransaction_date = datetime.strptime(ctransaction_date, '%Y-%m-%dT%H:%M')
            except ValueError:
                errors.append('Invalid Transaction Date format. Use YYYY-MM-DDTHH:MM format.')
        else:
            ctransaction_date = None 

        if errors:
            context = {
                'errors': errors,
            }
            return render(request, 'finance/transaction_add.html', context)

        query = OtherIncomeExpense(transaction_type=ctransaction_type, transaction_date=ctransaction_date, amount=camount, transaction_status=ctransaction_status, reason=creason, modified_date=cmodified_date)
        query.save()
        messages.success(request, "Transaction Added Successfully!")
        return redirect("/transaction")

    return render(request, 'finance/transaction_add.html')

@login_required(login_url='login')
def transaction_edit(request, id):
    if not request.user.has_perm('erp.change_transaction'):
        return HttpResponse('You are not authorised to view this page', status=403)
    edit = OtherIncomeExpense.objects.get(id=id)

    if request.method=="POST":
        ctransaction_type=request.POST.get('transaction_type')
        ctransaction_date=request.POST.get('transaction_date')
        camount=request.POST.get('amount')
        ctransaction_status=request.POST.get('transaction_status')
        creason=request.POST.get('reason')
        cmodified_date=datetime.now().date()

        errors = []
        if not ctransaction_type:
            errors.append('Transaction Type is required.')
        
        if not ctransaction_status:
            errors.append('Transaction Status is required.')

        if camount:
            try:
                camount = float(camount)
                if camount <= 0:
                    errors.append("Amount must be a positive number.")
            except ValueError:
                errors.append('Amount must be a number.')
        else:
            camount = None 

        if ctransaction_date:
            try:
                ctransaction_date = datetime.strptime(ctransaction_date, '%Y-%m-%dT%H:%M')
            except ValueError:
                errors.append('Invalid Transaction Date format. Use YYYY-MM-DDTHH:MM format.')
        else:
            ctransaction_date = None 

        if errors:
            context = {
                'errors': errors,
                'transaction':edit,
            }
            return render(request, 'finance/transaction_edit.html', context)
        
        edit.transaction_type = ctransaction_type
        edit.transaction_date = ctransaction_date
        edit.amount = camount
        edit.transaction_status = ctransaction_status
        edit.reason = creason
        edit.save()
        messages.success(request, "Transaction Updated Successfully!")
        return redirect("/transaction")
    
    context = {"transaction": edit}

    return render(request, 'finance/transaction_edit.html', context)

def transaction_delete(request, id):
    if not request.user.has_perm('erp.delete_transaction'):
        return HttpResponse('You are not authorised to view this page', status=403)
    d = OtherIncomeExpense.objects.get(id=id)
    d.delete()
    messages.error(request, "Transaction Deleted Successfully!")
    return redirect("/transaction")

def get_total_stock_value(queryset):
    return queryset.annotate(quantity_float=Cast('quantity', FloatField())
    ).aggregate(total_value=Sum(F('quantity_float') * F('current_unit_price')))['total_value'] or 0

def get_accounts_payable_value(queryset, year):
    approved_orders_current_year = Order.objects.filter(request_approved_date__year__lte=year)
    return queryset.filter(order__order__in=approved_orders_current_year).annotate(
        quantity_float=Cast('quantity', FloatField())
    ).aggregate(total_value=Sum(F('quantity_float') * F('price')))['total_value'] or 0

@login_required(login_url='login')
def balance_sheet(request):
    if not request.user.has_perm('erp.view_reports'):
        return HttpResponse('You are not authorised to view this page', status=403)
    current_year = now().year
    past_year = current_year - 1

    accounts_receivable_value = SalesOrder.objects.filter(payment_status='Not Paid',order_date__year__lte=current_year).aggregate(total_value=Sum('total_amount'))['total_value'] or 0
    other_income_value = OtherIncomeExpense.objects.filter(transaction_date__year__lte=current_year,transaction_type='Income',transaction_status='Pending').aggregate(total_value=Sum('amount'))['total_value'] or 0
    current_year_assets = {
        'cattle': Cattle.objects.filter(acquired_date__year__lte=current_year).aggregate(total_value=Sum('estimated_price'))['total_value'] or 0,
        'stock': get_total_stock_value(Stock.objects.all()),
        'accounts_receivable': accounts_receivable_value + other_income_value,
        'other_income': OtherIncomeExpense.objects.filter(transaction_date__year__lte=current_year, transaction_type='Income', transaction_status='Paid').aggregate(total_value=Sum('amount'))['total_value'] or 0,
    }
    current_year_total_assets = sum(current_year_assets.values())

    past_accounts_receivable_value = SalesOrder.objects.filter(payment_status='Not Paid',order_date__year__lte=past_year).aggregate(total_value=Sum('total_amount'))['total_value'] or 0
    past_other_income_value = OtherIncomeExpense.objects.filter(transaction_date__year__lte=past_year, transaction_type='Income', transaction_status='Pending').aggregate(total_value=Sum('amount'))['total_value'] or 0
    past_year_assets = {
        'cattle': Cattle.objects.filter(acquired_date__year__lte=past_year).aggregate(total_value=Sum('estimated_price'))['total_value'] or 0,
        'stock': 0,
        'accounts_receivable': past_accounts_receivable_value + past_other_income_value,
        'other_income': OtherIncomeExpense.objects.filter(transaction_date__year__lte=past_year, transaction_type='Income', transaction_status='Paid').aggregate(total_value=Sum('amount'))['total_value'] or 0,
    }
    past_year_total_assets = sum(past_year_assets.values())

    accounts_payable_value = get_accounts_payable_value(OrderHasItemSupplier.objects.filter(inventory_status='Pending'), current_year)
    other_expense_value = OtherIncomeExpense.objects.filter(transaction_date__year__lte=current_year,transaction_type='Expense',transaction_status='Pending').aggregate(total_value=Sum('amount'))['total_value'] or 0
    current_year_liabilities = {
        'other_expense': OtherIncomeExpense.objects.filter(transaction_date__year__lte=current_year, transaction_type='Expense', transaction_status='Paid').aggregate(total_value=Sum('amount'))['total_value'] or 0,
        'accounts_payable': accounts_payable_value + other_expense_value
    }
    current_year_total_liabilities = sum(current_year_liabilities.values())

    past_accounts_payable_value = get_accounts_payable_value(OrderHasItemSupplier.objects.filter(inventory_status='Pending'), past_year)
    past_other_expense_value = OtherIncomeExpense.objects.filter(transaction_date__year__lte=past_year,transaction_type='Expense',transaction_status='Pending').aggregate(total_value=Sum('amount'))['total_value'] or 0
    past_year_liabilities = {
        'other_expense': OtherIncomeExpense.objects.filter(transaction_date__year__lte=past_year, transaction_type='Expense', transaction_status='Paid').aggregate(total_value=Sum('amount'))['total_value'] or 0,
        'accounts_payable': past_accounts_payable_value + past_other_expense_value
    }
    past_year_total_liabilities = sum(past_year_liabilities.values())

    context = {
        'current_year': {
            'assets': current_year_assets,
            'total_assets': current_year_total_assets,
            'liabilities': current_year_liabilities,
            'total_liabilities': current_year_total_liabilities,
            'cyear':current_year,
        },
        'past_year': {
            'assets': past_year_assets,
            'total_assets': past_year_total_assets,
            'liabilities': past_year_liabilities,
            'total_liabilities': past_year_total_liabilities,
            'pyear':past_year,
        }
    }

    return render(request, 'finance/balance_sheet.html', context)

def get_procurement_value(queryset, start_date, end_date):
    approved_orders_current_year = Order.objects.filter(request_approved_date__range=[start_date, end_date])
    return queryset.filter(order__order__in=approved_orders_current_year).annotate(
        quantity_float=Cast('quantity', FloatField())
    ).aggregate(total_value=Sum(F('quantity_float') * F('price')))['total_value'] or 0


@login_required(login_url='login')
def profit_loss(request):
    if not request.user.has_perm('erp.view_reports'):
        return HttpResponse('You are not authorised to view this page', status=403)
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    current_year = datetime.now().year

    current_year_incomes = {}
    current_year_expenses = {}

    if start_date and end_date:
        current_year_incomes['sales_income'] = SalesOrder.objects.filter(
            payment_status='Fully Paid',
            order_date__range=[start_date, end_date]
        ).aggregate(total_value=Sum('total_amount'))['total_value'] or 0

        current_year_incomes['other_income'] = OtherIncomeExpense.objects.filter(
            transaction_date__range=[start_date, end_date],
            transaction_type='Income',
            transaction_status='Paid'
        ).aggregate(total_value=Sum('amount'))['total_value'] or 0


        current_year_expenses['procurement_expense'] = get_procurement_value(
            OrderHasItemSupplier.objects.filter(inventory_status='Approved'),
            start_date,
            end_date
        )

        current_year_expenses['stockin_expense'] = DirectlyAddedItem.objects.filter(
            added_date__range=[start_date, end_date],
            approval_status='Approved'
        ).aggregate(total_value=Sum('total_price'))['total_value'] or 0

        current_year_expenses['other_expense'] = OtherIncomeExpense.objects.filter(
            transaction_date__range=[start_date, end_date],
            transaction_type='Expense',
            transaction_status='Paid'
        ).aggregate(total_value=Sum('amount'))['total_value'] or 0

    elif start_date:
        current_year_incomes['sales_income'] = SalesOrder.objects.filter(
            payment_status='Fully Paid',
            order_date__range=[start_date, datetime.now().date()]
        ).aggregate(total_value=Sum('total_amount'))['total_value'] or 0

        current_year_incomes['other_income'] = OtherIncomeExpense.objects.filter(
            transaction_date__range=[start_date, datetime.now().date()],
            transaction_type='Income',
            transaction_status='Paid'
        ).aggregate(total_value=Sum('amount'))['total_value'] or 0


        current_year_expenses['procurement_expense'] = get_procurement_value(
            OrderHasItemSupplier.objects.filter(inventory_status='Approved'),
            start_date,
            datetime.now().date()  
        )

        current_year_expenses['stockin_expense'] = DirectlyAddedItem.objects.filter(
            added_date__range=[start_date, datetime.now().date()],
            approval_status='Approved'
        ).aggregate(total_value=Sum('total_price'))['total_value'] or 0

        current_year_expenses['other_expense'] = OtherIncomeExpense.objects.filter(
            transaction_date__range=[start_date, datetime.now().date()],
            transaction_type='Expense',
            transaction_status='Paid'
        ).aggregate(total_value=Sum('amount'))['total_value'] or 0

    elif end_date:

        current_year_incomes['sales_income'] = SalesOrder.objects.filter(
            payment_status='Fully Paid',
            order_date__lte=end_date
        ).aggregate(total_value=Sum('total_amount'))['total_value'] or 0

        current_year_incomes['other_income'] = OtherIncomeExpense.objects.filter(
            transaction_date__lte=end_date,
            transaction_type='Income',
            transaction_status='Paid'
        ).aggregate(total_value=Sum('amount'))['total_value'] or 0


        current_year_expenses['procurement_expense'] = get_procurement_value(
            OrderHasItemSupplier.objects.filter(inventory_status='Approved'),
            None,  
            end_date
        )

        current_year_expenses['stockin_expense'] = DirectlyAddedItem.objects.filter(
            added_date__lte=end_date,
            approval_status='Approved'
        ).aggregate(total_value=Sum('total_price'))['total_value'] or 0

        current_year_expenses['other_expense'] = OtherIncomeExpense.objects.filter(
            transaction_date__lte=end_date,
            transaction_type='Expense',
            transaction_status='Paid'
        ).aggregate(total_value=Sum('amount'))['total_value'] or 0

    current_year_total_incomes = sum(current_year_incomes.values())
    current_year_total_expenses = sum(current_year_expenses.values())
    profit = current_year_total_incomes - current_year_total_expenses

    context = {
        'current_year': {
            'incomes': current_year_incomes,
            'total_incomes': current_year_total_incomes,
            'expenses': current_year_expenses,
            'total_expenses': current_year_total_expenses,
            'profit': profit,
        },
        'filters_applied': bool(start_date or end_date),
    }
    return render(request, 'finance/profit_loss.html', context)

@login_required(login_url='login')
def reports(request):
    if not request.user.has_perm('erp.view_reports'):
        return HttpResponse('You are not authorised to view this page', status=403)
    return render(request, 'reports/reports.html')

@login_required(login_url='login')
def milk_production_report(request):
    if not request.user.has_perm('erp.view_reports'):
        return HttpResponse('You are not authorised to view this page', status=403)
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    cattle_id = request.GET.get('cattle')

    milk_production_data = MilkProduction.objects.all()

    if start_date:
        milk_production_data = milk_production_data.filter(milk_time__gte=start_date)
    if end_date:
        milk_production_data = milk_production_data.filter(milk_time__lte=end_date)
    if cattle_id:
        milk_production_data = milk_production_data.filter(cattle_id=cattle_id)

    cattle_list = Cattle.objects.filter(milkproduction__isnull=False).distinct()
    paginated_data = paginate_data(request, milk_production_data, 10) 

    context = {
        'milk_production_data': paginated_data,
        'cattle_list': cattle_list,
        'filters_applied': bool(start_date or end_date or cattle_id),
    }

    return render(request, 'reports/milk_production_report.html', context)

@login_required(login_url='login')
def total_milk_production_report(request):
    if not request.user.has_perm('erp.view_reports'):
        return HttpResponse('You are not authorised to view this page', status=403)
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    total_milk_production_data = MilkProduction.objects.all()

    if start_date:
        total_milk_production_data = total_milk_production_data.filter(milk_time__gte=start_date)
    if end_date:
        total_milk_production_data = total_milk_production_data.filter(milk_time__lte=end_date)

    total_amount = total_milk_production_data.aggregate(total=Sum('amount_in_liter'))['total'] or 0

    paginated_data = paginate_data(request, total_milk_production_data, 10) 

    context = {
        'total_milk_production_data': paginated_data,
        'total_amount': total_amount,
        'filters_applied': bool(start_date or end_date),
    }

    return render(request, 'reports/total_milk_production_report.html', context)


@login_required(login_url='login')
def stock_report(request):
    if not request.user.has_perm('erp.view_reports'):
        return HttpResponse('You are not authorised to view this page', status=403)
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    item_id = request.GET.get('item')

    stock_data = Stock.objects.all()

    if start_date:
        stock_data = stock_data.filter(modified_date__gte=start_date)
    if end_date:
        stock_data = stock_data.filter(modified_date__lte=end_date)
    if item_id:
        stock_data = stock_data.filter(item_id=item_id)

    item_list = Item.objects.filter(stock__isnull=False).distinct()
    paginated_data = paginate_data(request, stock_data, 10) 

    context = {
        'item_list': item_list,
        'filters_applied': bool(start_date or end_date or item_id),
        'stock_data': paginated_data,
    }

    return render(request, 'reports/stock_report.html', context)

@login_required(login_url='login')
def sales_report(request):
    if not request.user.has_perm('erp.view_reports'):
        return HttpResponse('You are not authorised to view this page', status=403)
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    sales_data = SalesOrder.objects.all()

    if start_date:
        sales_data = sales_data.filter(order_date__gte=start_date)
    if end_date:
        sales_data = sales_data.filter(order_date__lte=end_date)

    paginated_data = paginate_data(request, sales_data, 10) 

    context = {
        'sales_data': paginated_data,
        'filters_applied': bool(start_date or end_date),
    }

    return render(request, 'reports/sales_report.html', context)

@login_required(login_url='login')
def procurement_report(request):
    if not request.user.has_perm('erp.view_reports'):
        return HttpResponse('You are not authorised to view this page', status=403)
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    procurement_data = OrderHasItemSupplier.objects.filter(status="Approved")

    if start_date:
        procurement_data = procurement_data.filter(modified_date__gte=start_date)
    if end_date:
        procurement_data = procurement_data.filter(modified_date__lte=end_date)

    paginated_data = paginate_data(request, procurement_data, 10) 

    context = {
        'procurement_data': paginated_data,
        'filters_applied': bool(start_date or end_date),
    }

    return render(request, 'reports/procurement_report.html', context)

@login_required(login_url='login')
def feed_formulation_report(request):
    if not request.user.has_perm('erp.view_reports'):
        return HttpResponse('You are not authorised to view this page', status=403)
    formulation_data = FeedFormulation.objects.all()
    paginated_data = paginate_data(request, formulation_data, 10) 

    context = {
        'formulation_data': paginated_data,
    }

    return render(request, 'reports/feed_formulation_report.html', context)

@login_required(login_url='login')
def employee_report(request):
    if not request.user.has_perm('erp.view_reports'):
        return HttpResponse('You are not authorised to view this page', status=403)
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    employee_id = request.GET.get('employee')

    employee_data = Employee.objects.all()

    if start_date:
        employee_data = employee_data.filter(hire_date__gte=start_date)
    if end_date:
        employee_data = employee_data.filter(hire_date__lte=end_date)
    if employee_id:
        employee_data = employee_data.filter(person_farm_entity_id=employee_id)

    paginated_data = paginate_data(request, employee_data, 10) 

    context = {
        'employee_data': paginated_data,
        'filters_applied': bool(start_date or end_date or employee_id),
    }

    return render(request, 'reports/employee_report.html', context)


@login_required(login_url='login')
def employee_with_task_report(request):
    if not request.user.has_perm('erp.view_reports'):
        return HttpResponse('You are not authorised to view this page', status=403)
    today = timezone.now().date()
    task_data = TaskAssignment.objects.filter(due_time__date=today)
    paginated_data = paginate_data(request, task_data, 10) 

    context = {
        'task_data': paginated_data,
    }

    return render(request, 'reports/employee_with_task_report.html', context)



