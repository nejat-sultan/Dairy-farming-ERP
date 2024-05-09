from datetime import datetime
import os
from django.shortcuts import get_object_or_404, render,redirect
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.http import JsonResponse


from testproject import settings
from .models import CattleBreed, CattlePhoto, CattlePregnancy, CattleStatus, ContactType, Dashboard, FarmEntity, FeedFormulation, GuaranteeType, Item, Job, MilkProduction, Order, OrderHasItem, OrderHasItemSupplier, PersonTitle, PersonType, Region, SaleType, Shift, Supplier, SupplierType, Vaccine
from .models import Cattle
from django.contrib import messages

# Create your views here.

def index(request):
    dash1 = Dashboard()
    dash1.amount = 100
    dash1.description = 'Purchase Orders'

    dash2 = Dashboard()
    dash2.amount = 50
    dash2.description = 'Stock Available'

    dash3 = Dashboard()
    dash3.amount = 300
    dash3.description = 'Users'

    dash4 = Dashboard()
    dash4.amount = 400
    dash4.description = 'Unique Visitors'

    # dashs = [dash1, dash2, dash3, dash4]

    return render(request, 'index.html',{'dash1': dash1, 'dash2': dash2, 'dash3': dash3, 'dash4': dash4})

def cattle(request):
    data = Cattle.objects.all()
    context = {"data":data}

    return render(request, 'cattle/cattle.html', context)

def cattle_view(request, cattle_id):

    cattle = get_object_or_404(Cattle, cattle_id=cattle_id)
    photos = CattlePhoto.objects.filter(cattle=cattle)
    breeds = CattleBreed.objects.filter(cattle=cattle)
    statuses = CattlePregnancy.objects.filter(cattle=cattle).order_by('-cattle_id')[:1]
    productions = MilkProduction.objects.filter(cattle=cattle).order_by('-cattle_id')[:1]

    context = {
        'cattle': cattle,
        'photos': photos,
        'breeds': breeds,
        'statuses': statuses,
        'productions': productions
    }

    return render(request, 'cattle/cattle_view.html', context)


def cattle_add(request):
    if request.method=="POST":
        cid=request.POST.get('id')
        cdob=request.POST.get('dob')
        cname=request.POST.get('name')
        cgender=request.POST.get('gender')
        cestimatedprice=request.POST.get('estimated_price')
        cbreed=request.POST.get('breed')
        cstatus=request.POST.get('status')

        query = Cattle(cattle_id=cid, cattle_date_of_birth=cdob, cattle_name=cname, cattle_gender=cgender, estimated_price=cestimatedprice, cattle_breed_id=cbreed, cattle_status_id=cstatus)
        query.save()
        messages.info(request, "Cattle Added Successfully!")
        return redirect("/cattle")

    breed_data = CattleBreed.objects.all()
    data = CattleStatus.objects.all()
    cattle_data = Cattle.objects.all()

    context = {
        'data1': data,
        'data2': cattle_data,
        'data3': breed_data,
    }

    return render(request, 'cattle/cattle_add.html', context)

def cattle_edit(request,cattle_id):

    # Fetch the cattle object by its id
    edit = Cattle.objects.get(cattle_id=cattle_id)
    
    if request.method == "POST":
        cid=request.POST.get('id')
        cdob=request.POST.get('dob')
        cname=request.POST.get('name')
        cgender=request.POST.get('gender')
        cestimatedprice=request.POST.get('estimated_price')
        cbreed=request.POST.get('breed')
        cstatus=request.POST.get('status')
        
        # Update the attributes
        edit.cattle_id = cid
        edit.cattle_date_of_birth = cdob
        edit.cattle_name = cname
        edit.cattle_gender = cgender
        edit.estimated_price = cestimatedprice
        edit.cattle_breed_id = cbreed
        edit.cattle_status_id = cstatus
        
        # Save the changes
        edit.save()
        messages.warning(request, "Cattle Updated Successfully!")
        # Optionally, redirect to a success page or another view
        return redirect("/cattle")
    
    # Fetch all cattle statuses
    cattle_statuses = CattleStatus.objects.all()

    cattle_breed = CattleBreed.objects.all()
    context = {"cattle": edit, "cattle_statuses": cattle_statuses, "cattle_breed": cattle_breed}

    return render(request, 'cattle/cattle_edit.html', context)

def cattle_delete(request, cattle_id):
    d = Cattle.objects.get(cattle_id=cattle_id)
    d.delete()
    messages.error(request, "Cattle Deleted Successfully!")
    return redirect("/cattle")

# Django view function to handle adding a photo
def add_photo(request):

    if request.method == 'POST':
        # Retrieve photo form data
        cattle_id = request.POST.get('cattle_id')
        photo_description = request.POST.get('photo_description')

        # Handle file upload
        if 'photo_url' in request.FILES:
            photo_file = request.FILES['photo_url']

            fs = FileSystemStorage(location=settings.MEDIA_ROOT + '/photos')
            filename = fs.save(photo_file.name, photo_file)
            # Construct the photo URL including the 'photos' directory
            photo_url = settings.MEDIA_URL + 'photos/' + filename
            
            
            # Create a new CattlePhoto instance
            photo = CattlePhoto(
                cattle_id=cattle_id,
                cattle_photo_url=photo_url,
                cattle_photo_description=photo_description
            )
            photo.save()

            messages.info(request, "Cattle Photo Added Successfully!")
            return redirect("/cattle")
        
    data = CattleStatus.objects.all()
    cattle_data = Cattle.objects.all()

    context = {
        'data1': data,
        'data2': cattle_data,
    }

    return render(request, 'cattle/cattle_add.html', context)

def cattle_status(request):
    data = CattleStatus.objects.all()
    context = {"data1":data}

    return render(request, 'cattle/cattle_status.html', context)

def cattle_status_add(request):
    if request.method=="POST":
        cstatus=request.POST.get('status')

        query = CattleStatus(cattle_status=cstatus)
        query.save()
        messages.info(request, "Cattle Status Added Successfully!")
        return redirect("/cattle_status")

    return render(request, 'cattle/cattle_status_add.html')

def cattle_status_edit(request,cattle_status_id):
    # Fetch the cattle object by its id
    edit = CattleStatus.objects.get(cattle_status_id=cattle_status_id)
    
    if request.method == "POST":
        cstatus=request.POST.get('status')
        
        # Update the attributes
        edit.cattle_status = cstatus
        
        # Save the changes
        edit.save()
        messages.warning(request, "Cattle Status Updated Successfully!")
        # Optionally, redirect to a success page or another view
        return redirect("/cattle_status")

    # Fetch the cattle object again for rendering the form
    d = CattleStatus.objects.get(cattle_status_id=cattle_status_id)
    context = {"d": d}

    return render(request, 'cattle/cattle_status_edit.html', context)

def cattle_status_delete(request, cattle_status_id):
    d = CattleStatus.objects.get(cattle_status_id=cattle_status_id)
    d.delete()
    messages.error(request, "Cattle Status Deleted Successfully!")
    return redirect("/cattle_status")

def cattle_breed(request):
    data = CattleBreed.objects.all()
    context = {"data1":data}

    return render(request, 'cattle/cattle_breed.html', context)

def cattle_breed_add(request):
    if request.method=="POST":
        cbreed_type=request.POST.get('breed_type')
        cbreed_description=request.POST.get('breed_description')

        query = CattleBreed(cattle_breed_type=cbreed_type, cattle_breed_description=cbreed_description)
        query.save()
        messages.info(request, "Cattle Breed Added Successfully!")
        return redirect("/cattle_breed")

    return render(request, 'cattle/cattle_breed_add.html')

def cattle_breed_edit(request,cattle_breed_id):
    # Fetch the cattle object by its id
    edit = CattleBreed.objects.get(cattle_breed_id=cattle_breed_id)
    
    if request.method == "POST":
        cbreed_type=request.POST.get('breed_type')
        cbreed_description=request.POST.get('breed_description')
        
        # Update the attributes
        edit.cattle_breed_type = cbreed_type
        edit.cattle_breed_description = cbreed_description
        
        # Save the changes
        edit.save()
        messages.warning(request, "Cattle Breed Updated Successfully!")
        # Optionally, redirect to a success page or another view
        return redirect("/cattle_breed")

    # Fetch the cattle object again for rendering the form
    d = CattleBreed.objects.get(cattle_breed_id=cattle_breed_id)
    context = {"d": d}

    return render(request, 'cattle/cattle_breed_edit.html', context)

def cattle_breed_delete(request, cattle_breed_id):
    d = CattleBreed.objects.get(cattle_breed_id=cattle_breed_id)
    d.delete()
    messages.error(request, "Cattle Breed Deleted Successfully!")
    return redirect("/cattle_breed")

def cattle_pregnancy(request):
    data = CattlePregnancy.objects.all()
    cattle = Cattle.objects.all()

    context = {"data1":data, 'cattle': cattle,}

    return render(request, 'cattle/cattle_pregnancy.html', context)

def cattle_pregnancy_add(request):
    if request.method=="POST":
        cpregnancy_type=request.POST.get('pregnancy_type')
        cpregnancy_date=request.POST.get('pregnancy_date')
        ccattle_id=request.POST.get('cattle_id')
        cpregnancy_status = "Pregnant"

        query = CattlePregnancy(cattle_pregnancy_type=cpregnancy_type, cattle_pregnancy_date=cpregnancy_date, cattle_id=ccattle_id, cattle_pregnancy_status=cpregnancy_status)
        query.save()
        messages.info(request, "Cattle Pregnancy Added Successfully!")
        return redirect("/cattle_pregnancy")
    
    cattle_data = Cattle.objects.all()

    context = {
        'data1': cattle_data,
    }

    return render(request, 'cattle/cattle_pregnancy_add.html', context)

def cattle_pregnancy_edit(request,cattle_pregnancy_id):
    # Fetch the cattle object by its id
    edit = CattlePregnancy.objects.get(cattle_pregnancy_id=cattle_pregnancy_id)
    
    if request.method == "POST":
        cpregnancy_type=request.POST.get('pregnancy_type')
        cpregnancy_date=request.POST.get('pregnancy_date')
        ccattle_id=request.POST.get('cattle_id')
        cpregnancy_status=request.POST.get('pregnancy_status')
        
        # Update the attributes
        edit.cattle_pregnancy_type = cpregnancy_type
        edit.cattle_pregnancy_date = cpregnancy_date
        edit.cattle_id = ccattle_id
        edit.cattle_pregnancy_status = cpregnancy_status
        
        # Save the changes
        edit.save()
        messages.warning(request, "Cattle Pregnancy Updated Successfully!")
        # Optionally, redirect to a success page or another view
        return redirect("/cattle_pregnancy")
    

    # Fetch the cattle object again for rendering the form
    d = CattlePregnancy.objects.get(cattle_pregnancy_id=cattle_pregnancy_id)
    cattles = Cattle.objects.all()
    context = {"d": d, "cattle": edit, "cattles": cattles}

    return render(request, 'cattle/cattle_pregnancy_edit.html', context)

def cattle_pregnancy_delete(request, cattle_pregnancy_id):
    d = CattlePregnancy.objects.get(cattle_pregnancy_id=cattle_pregnancy_id)
    d.delete()
    messages.error(request, "Cattle Pregnancy Deleted Successfully!")
    return redirect("/cattle_pregnancy")

def vaccine(request):
    data = Vaccine.objects.all()
    context = {"data1":data}

    return render(request, 'cattle/vaccine.html', context)

def vaccine_add(request):
    if request.method=="POST":
        cvaccine_name=request.POST.get('vaccine_name')
        cvaccine_benefit=request.POST.get('vaccine_benefit')
        cvaccine_recommended_time=request.POST.get('vaccine_recommended_time')

        query = Vaccine(vaccine_name=cvaccine_name, vaccine_benefit=cvaccine_benefit, vaccine_recommended_time=cvaccine_recommended_time)
        query.save()
        messages.info(request, "Vaccine Added Successfully!")
        return redirect("/vaccine")

    return render(request, 'cattle/vaccine_add.html')

def vaccine_edit(request,vaccine_id):
    # Fetch the vaccine object by its id
    edit = Vaccine.objects.get(vaccine_id=vaccine_id)
    
    if request.method == "POST":
        cvaccine_name=request.POST.get('vaccine_name')
        cvaccine_benefit=request.POST.get('vaccine_benefit')
        cvaccine_recommended_time=request.POST.get('vaccine_recommended_time')
        
        # Update the attributes
        edit.vaccine_name = cvaccine_name
        edit.vaccine_benefit = cvaccine_benefit
        edit.vaccine_recommended_time = cvaccine_recommended_time
        
        # Save the changes
        edit.save()
        messages.warning(request, "Vaccine Updated Successfully!")
        # Optionally, redirect to a success page or another view
        return redirect("/vaccine")

    # Fetch the vaccine object again for rendering the form
    d = Vaccine.objects.get(vaccine_id=vaccine_id)
    context = {"d": d}

    return render(request, 'cattle/vaccine_edit.html', context)

def vaccine_delete(request, vaccine_id):
    d = Vaccine.objects.get(vaccine_id=vaccine_id)
    d.delete()
    messages.error(request, "Vaccine Deleted Successfully!")
    return redirect("/vaccine")

def milk_production(request):
    data = MilkProduction.objects.all()
    cattle = Cattle.objects.all()

    context = {"data1":data, 'cattle': cattle,}

    return render(request, 'cattle/milk_production.html', context)

def milk_production_add(request):
    if request.method=="POST":
        camount_in_liter=request.POST.get('amount_in_liter')
        cmilk_time=request.POST.get('milk_time')
        cfat_content=request.POST.get('fat_content')
        cprotein_content=request.POST.get('protein_content')
        csomatic_cell_count=request.POST.get('somatic_cell_count')
        cduration_in_min=request.POST.get('duration_in_min')
        ccattle_id=request.POST.get('cattle_id')

        query = MilkProduction(amount_in_liter=camount_in_liter, milk_time=cmilk_time, fat_content=cfat_content, protein_content=cprotein_content, somatic_cell_count=csomatic_cell_count, duration_in_min=cduration_in_min, cattle_id=ccattle_id)
        query.save()
        messages.info(request, "Milk Production Added Successfully!")
        return redirect("/milk_production")
    
    cattle_data = Cattle.objects.all()
    context = {
        'data2': cattle_data,
    }

    return render(request, 'cattle/milk_production_add.html',context)

def milk_production_edit(request,milk_production_id):
    # Fetch the vaccine object by its id
    edit = MilkProduction.objects.get(milk_production_id=milk_production_id)
    
    if request.method == "POST":
        camount_in_liter=request.POST.get('amount_in_liter')
        cmilk_time=request.POST.get('milk_time')
        cfat_content=request.POST.get('fat_content')
        cprotein_content=request.POST.get('protein_content')
        csomatic_cell_count=request.POST.get('somatic_cell_count')
        cduration_in_min=request.POST.get('duration_in_min')
        ccattle_id=request.POST.get('cattle_id')
        
        # Update the attributes
        edit.amount_in_liter = camount_in_liter
        edit.milk_time = cmilk_time
        edit.fat_content = cfat_content
        edit.protein_content = cprotein_content
        edit.somatic_cell_count = csomatic_cell_count
        edit.duration_in_min = cduration_in_min
        edit.cattle_id = ccattle_id
        
        # Save the changes
        edit.save()
        messages.warning(request, "Milk Production Updated Successfully!")
        # Optionally, redirect to a success page or another view
        return redirect("/milk_production")

    # Fetch the vaccine object again for rendering the form
    d = MilkProduction.objects.get(milk_production_id=milk_production_id)
    cattles = Cattle.objects.all()
    context = {"d": d, "cattle": edit, "cattles": cattles}

    return render(request, 'cattle/milk_production_edit.html', context)

def milk_production_delete(request, milk_production_id):
    d = MilkProduction.objects.get(milk_production_id=milk_production_id)
    d.delete()
    messages.error(request, "Milk Production Deleted Successfully!")
    return redirect("/milk_production")


def person_type(request):
    data = PersonType.objects.all()
    context = {"data1":data}

    return render(request, 'person/person_type.html', context)

def person_type_add(request):
    if request.method=="POST":
        cperson_type=request.POST.get('person_type')

        query = PersonType(person_type=cperson_type)
        query.save()
        messages.info(request, "Person Type Added Successfully!")
        return redirect("/person_type")

    return render(request, 'person/person_type_add.html')

def person_type_edit(request,person_type_id):
    edit = PersonType.objects.get(person_type_id=person_type_id)
    
    if request.method == "POST":
        cperson_type=request.POST.get('person_type')
        
        # Update the attributes
        edit.person_type = cperson_type
        
        # Save the changes
        edit.save()
        messages.warning(request, "Person Type Updated Successfully!")
        # Optionally, redirect to a success page or another view
        return redirect("/person_type")

    d = PersonType.objects.get(person_type_id=person_type_id)
    context = {"d": d}

    return render(request, 'person/person_type_edit.html', context)

def person_type_delete(request, person_type_id):
    d = PersonType.objects.get(person_type_id=person_type_id)
    d.delete()
    messages.error(request, "Person Type Deleted Successfully!")
    return redirect("/person_type")

def person_title(request):
    data = PersonTitle.objects.all()
    context = {"data1":data}

    return render(request, 'person/person_title.html', context)

def person_title_add(request):
    if request.method=="POST":
        cperson_title=request.POST.get('person_title')

        query = PersonTitle(person_title=cperson_title)
        query.save()
        messages.info(request, "Person Title Added Successfully!")
        return redirect("/person_title")

    return render(request, 'person/person_title_add.html')

def person_title_edit(request,person_title_id):
    edit = PersonTitle.objects.get(person_title_id=person_title_id)
    
    if request.method == "POST":
        cperson_title=request.POST.get('person_title')
        
        # Update the attributes
        edit.person_title = cperson_title
        
        # Save the changes
        edit.save()
        messages.warning(request, "Person Title Updated Successfully!")
        # Optionally, redirect to a success page or another view
        return redirect("/person_title")

    d = PersonTitle.objects.get(person_title_id=person_title_id)
    context = {"d": d}

    return render(request, 'person/person_title_edit.html', context)

def person_title_delete(request, person_title_id):
    d = PersonTitle.objects.get(person_title_id=person_title_id)
    d.delete()
    messages.error(request, "Person Title Deleted Successfully!")
    return redirect("/person_title")

def contact_type(request):
    data = ContactType.objects.all()
    context = {"data1":data}

    return render(request, 'person/contact_type.html', context)

def contact_type_add(request):
    if request.method=="POST":
        ccontact_type=request.POST.get('contact_type')
        ccontact_type_desc=request.POST.get('description')

        query = ContactType(contact_type=ccontact_type, contact_type_desc=ccontact_type_desc)
        query.save()
        messages.info(request, "Contact Type Added Successfully!")
        return redirect("/contact_type")

    return render(request, 'person/contact_type_add.html')

def contact_type_edit(request,contact_id):
    edit = ContactType.objects.get(contact_id=contact_id)
    
    if request.method == "POST":
        ccontact_type=request.POST.get('contact_type')
        ccontact_type_desc=request.POST.get('description')
        
        # Update the attributes
        edit.contact_type = ccontact_type
        edit.contact_type_desc = ccontact_type_desc
        
        # Save the changes
        edit.save()
        messages.warning(request, "Contact Type Updated Successfully!")
        # Optionally, redirect to a success page or another view
        return redirect("/contact_type")

    d = ContactType.objects.get(contact_id=contact_id)
    context = {"d": d}

    return render(request, 'person/contact_type_edit.html', context)

def contact_type_delete(request, contact_id):
    d = ContactType.objects.get(contact_id=contact_id)
    d.delete()
    messages.error(request, "Contact Type Deleted Successfully!")
    return redirect("/contact_type")

def sale_type(request):
    data = SaleType.objects.all()
    context = {"data1":data}

    return render(request, 'sales/sale_type.html', context)

def sale_type_add(request):
    if request.method=="POST":
        csale_type=request.POST.get('sale_type')

        query = SaleType(sale_type=csale_type)
        query.save()
        messages.info(request, "Sale Type Added Successfully!")
        return redirect("/sale_type")

    return render(request, 'sales/sale_type_add.html')

def sale_type_edit(request,sale_type_id):
    edit = SaleType.objects.get(sale_type_id=sale_type_id)
    
    if request.method == "POST":
        csale_type=request.POST.get('sale_type')
        
        # Update the attributes
        edit.sale_type = csale_type
        
        # Save the changes
        edit.save()
        messages.warning(request, "Sale Type Updated Successfully!")
        # Optionally, redirect to a success page or another view
        return redirect("/sale_type")

    d = SaleType.objects.get(sale_type_id=sale_type_id)
    context = {"d": d}

    return render(request, 'sales/sale_type_edit.html', context)

def sale_type_delete(request, sale_type_id):
    d = SaleType.objects.get(sale_type_id=sale_type_id)
    d.delete()
    messages.error(request, "Sale Type Deleted Successfully!")
    return redirect("/sale_type")

def region(request):
    data = Region.objects.all()
    context = {"data1":data}

    return render(request, 'region.html', context)

def region_add(request):
    if request.method=="POST":
        cregion=request.POST.get('region')

        query = Region(region=cregion)
        query.save()
        messages.info(request, "Region Added Successfully!")
        return redirect("/region")

    return render(request, 'region_add.html')

def region_edit(request,region_id):
    edit = Region.objects.get(region_id=region_id)
    
    if request.method == "POST":
        cregion=request.POST.get('region')
        
        # Update the attributes
        edit.region = cregion
        
        # Save the changes
        edit.save()
        messages.warning(request, "Region Updated Successfully!")
        # Optionally, redirect to a success page or another view
        return redirect("/region")

    d = Region.objects.get(region_id=region_id)
    context = {"d": d}

    return render(request, 'region_edit.html', context)

def region_delete(request, region_id):
    d = Region.objects.get(region_id=region_id)
    d.delete()
    messages.error(request, "Region Deleted Successfully!")
    return redirect("/region")


def guarantee_type(request):
    data = GuaranteeType.objects.all()
    context = {"data1":data}

    return render(request, 'guarantee_type.html', context)

def guarantee_type_add(request):
    if request.method=="POST":
        cguarantee_type=request.POST.get('guarantee_type')

        query = GuaranteeType(guarantee_type=cguarantee_type)
        query.save()
        messages.info(request, "Guarantee Type Added Successfully!")
        return redirect("/guarantee_type")

    return render(request, 'guarantee_type_add.html')

def guarantee_type_edit(request,guarantee_type_id):
    edit = GuaranteeType.objects.get(guarantee_type_id=guarantee_type_id)
    
    if request.method == "POST":
        cguarantee_type=request.POST.get('guarantee_type')
        
        # Update the attributes
        edit.guarantee_type = cguarantee_type
        
        # Save the changes
        edit.save()
        messages.warning(request, "Guarantee Type Updated Successfully!")
        # Optionally, redirect to a success page or another view
        return redirect("/guarantee_type")

    d = GuaranteeType.objects.get(guarantee_type_id=guarantee_type_id)
    context = {"d": d}

    return render(request, 'guarantee_type_edit.html', context)

def guarantee_type_delete(request, guarantee_type_id):
    d = GuaranteeType.objects.get(guarantee_type_id=guarantee_type_id)
    d.delete()
    messages.error(request, "Guarantee Type Deleted Successfully!")
    return redirect("/guarantee_type")

def shift(request):
    data = Shift.objects.all()
    context = {"data1":data}

    return render(request, 'shift.html', context)

def shift_add(request):
    if request.method=="POST":
        cshift_name=request.POST.get('shift_name')
        cshift_start_time=request.POST.get('shift_start_time')
        cshift_end_time=request.POST.get('shift_end_time')

        query = Shift(shift_name=cshift_name, shift_start_time=cshift_start_time, shift_end_time=cshift_end_time)
        query.save()
        messages.info(request, "Shift Added Successfully!")
        return redirect("/shift")

    return render(request, 'shift_add.html')

def shift_edit(request,shift_id):
    edit = Shift.objects.get(shift_id=shift_id)
    
    if request.method == "POST":
        cshift_name=request.POST.get('shift_name')
        cshift_start_time=request.POST.get('shift_start_time')
        cshift_end_time=request.POST.get('shift_end_time')
        
        # Update the attributes
        edit.shift_name = cshift_name
        edit.shift_start_time = cshift_start_time
        edit.shift_end_time = cshift_end_time
        
        # Save the changes
        edit.save()
        messages.warning(request, "Shift Updated Successfully!")
        # Optionally, redirect to a success page or another view
        return redirect("/shift")

    d = Shift.objects.get(shift_id=shift_id)
    context = {"d": d}

    return render(request, 'shift_edit.html', context)

def shift_delete(request, shift_id):
    d = Shift.objects.get(shift_id=shift_id)
    d.delete()
    messages.error(request, "Shift Deleted Successfully!")
    return redirect("/shift")

def job(request):
    data = Job.objects.all()
    context = {"data1":data}

    return render(request, 'job.html', context)

def job_add(request):
    if request.method=="POST":
        cjob_title=request.POST.get('job_title')
        cjob_min_salary=request.POST.get('job_min_salary')
        cjob_max_salary=request.POST.get('job_max_salary')

        query = Job(job_title=cjob_title, job_min_salary=cjob_min_salary, job_max_salary=cjob_max_salary)
        query.save()
        messages.info(request, "Job Added Successfully!")
        return redirect("/job")

    return render(request, 'job_add.html')

def job_edit(request,job_id):
    edit = Job.objects.get(job_id=job_id)
    
    if request.method == "POST":
        cjob_title=request.POST.get('job_title')
        cjob_min_salary=request.POST.get('job_min_salary')
        cjob_max_salary=request.POST.get('job_max_salary')
        
        # Update the attributes
        edit.job_title = cjob_title
        edit.job_min_salary = cjob_min_salary
        edit.job_max_salary = cjob_max_salary
        
        # Save the changes
        edit.save()
        messages.warning(request, "Job Updated Successfully!")
        # Optionally, redirect to a success page or another view
        return redirect("/job")

    d = Job.objects.get(job_id=job_id)
    context = {"d": d}

    return render(request, 'job_edit.html', context)

def job_delete(request, job_id):
    d = Job.objects.get(job_id=job_id)
    d.delete()
    messages.error(request, "Job Deleted Successfully!")
    return redirect("/job")

def feed_formulation(request):
    data = FeedFormulation.objects.all()
    context = {"data1":data}

    return render(request, 'cattle/feed_formulation.html', context)

def feed_formulation_add(request):
    if request.method=="POST":
        cfeed_formulation_description=request.POST.get('feed_formulation_description')

        query = FeedFormulation(feed_formulation_description=cfeed_formulation_description)
        query.save()
        messages.info(request, "Feed Formulation Added Successfully!")
        return redirect("/feed_formulation")

    return render(request, 'cattle/feed_formulation_add.html')

def feed_formulation_edit(request,feed_formulation_id):
    edit = FeedFormulation.objects.get(feed_formulation_id=feed_formulation_id)
    
    if request.method == "POST":
        cfeed_formulation_description=request.POST.get('feed_formulation_description')
        
        # Update the attributes
        edit.feed_formulation_description = cfeed_formulation_description
        
        # Save the changes
        edit.save()
        messages.warning(request, "Feed Formulation Updated Successfully!")
        # Optionally, redirect to a success page or another view
        return redirect("/feed_formulation")

    d = FeedFormulation.objects.get(feed_formulation_id=feed_formulation_id)
    context = {"d": d}

    return render(request, 'cattle/feed_formulation_edit.html', context)

def feed_formulation_delete(request, feed_formulation_id):
    d = FeedFormulation.objects.get(feed_formulation_id=feed_formulation_id)
    d.delete()
    messages.error(request, "Feed Formulation Deleted Successfully!")
    return redirect("/feed_formulation")

def item(request):
    data = Item.objects.all()
    context = {"data1":data}

    return render(request, 'procurement/item.html', context)

def item_add(request):
    if request.method=="POST":
        cname=request.POST.get('name')

        query = Item(name=cname)
        query.save()
        messages.info(request, "Item Added Successfully!")
        return redirect("/item")

    return render(request, 'procurement/item_add.html')

def item_edit(request,item_id):
    edit = Item.objects.get(item_id=item_id)
    
    if request.method == "POST":
        cname=request.POST.get('name')
        
        # Update the attributes
        edit.name = cname
        
        # Save the changes
        edit.save()
        messages.warning(request, "Item Updated Successfully!")
        # Optionally, redirect to a success page or another view
        return redirect("/item")

    d = Item.objects.get(item_id=item_id)
    context = {"d": d}

    return render(request, 'procurement/item_edit.html', context)

def item_delete(request, item_id):
    d = Item.objects.get(item_id=item_id)
    d.delete()
    messages.error(request, "Item Deleted Successfully!")
    return redirect("/item")

def supplier_type(request):
    data = SupplierType.objects.all()
    context = {"data1":data}

    return render(request, 'procurement/supplier_type.html', context)

def supplier_type_add(request):
    if request.method=="POST":
        csupplier_type=request.POST.get('supplier_type')

        query = SupplierType(supplier_type=csupplier_type)
        query.save()
        messages.info(request, "Supplier Type Added Successfully!")
        return redirect("/supplier_type")

    return render(request, 'procurement/supplier_type_add.html')

def supplier_type_edit(request,supplier_type_id):
    edit = SupplierType.objects.get(supplier_type_id=supplier_type_id)
    
    if request.method == "POST":
        csupplier_type=request.POST.get('supplier_type')
        
        # Update the attributes
        edit.supplier_type = csupplier_type
        
        # Save the changes
        edit.save()
        messages.warning(request, "Supplier Type Updated Successfully!")
        # Optionally, redirect to a success page or another view
        return redirect("/supplier_type")

    d = SupplierType.objects.get(supplier_type_id=supplier_type_id)
    context = {"d": d}

    return render(request, 'procurement/supplier_type_edit.html', context)

def supplier_type_delete(request, supplier_type_id):
    d = SupplierType.objects.get(supplier_type_id=supplier_type_id)
    d.delete()
    messages.error(request, "Supplier Type Deleted Successfully!")
    return redirect("/supplier_type")

def supplier(request):
    data = Supplier.objects.all()
    type_data = SupplierType.objects.all()

    context = {"data1":data, 'type_data': type_data,}

    return render(request, 'procurement/supplier.html', context)

def supplier_add(request):
    if request.method == "POST":
        csupplier_name = request.POST.get('supplier_name')
        csupplier_type = request.POST.get('supplier_type')
        caccount_number = request.POST.get('account_number')

        # Create a new FarmEntity
        farm_entity = FarmEntity.objects.create(modified_date=timezone.now())

        # Create the Supplier instance and associate it with the FarmEntity
        supplier = Supplier.objects.create(
            farm_entity=farm_entity,
            supplier_name=csupplier_name,
            supplier_type_id=csupplier_type,
            account_number=caccount_number
        )

        messages.info(request, "Supplier Added Successfully!")
        return redirect("/supplier")
    
    # Fetch data for supplier type dropdown
    type_data = SupplierType.objects.all()
    context = {
        'data1': type_data,
    }

    return render(request, 'procurement/supplier_add.html', context)

def supplier_edit(request,farm_entity_id):
    edit = Supplier.objects.get(farm_entity_id=farm_entity_id)
    
    if request.method == "POST":
        csupplier_name = request.POST.get('supplier_name')
        csupplier_type = request.POST.get('supplier_type')
        caccount_number = request.POST.get('account_number')
        
        # Update the attributes
        edit.supplier_name = csupplier_name
        edit.supplier_type_id = csupplier_type
        edit.account_number = caccount_number
        
        # Save the changes
        edit.save()
        messages.warning(request, "Supplier Updated Successfully!")
        # Optionally, redirect to a success page or another view
        return redirect("/supplier")

    d = Supplier.objects.get(farm_entity_id=farm_entity_id)
    data1 = SupplierType.objects.all()
    context = {"d": d, "type": edit, "data1": data1}

    return render(request, 'procurement/supplier_edit.html', context)

def supplier_delete(request, farm_entity_id):
    d = Supplier.objects.get(farm_entity_id=farm_entity_id)
    d.delete()
    messages.error(request, "Supplier Deleted Successfully!")
    return redirect("/supplier")


def request_order(request):
    data = OrderHasItem.objects.all()
    orderdatas = Order.objects.all()
    item_data = Item.objects.all()

    context = {"data1":data,'orderdatas': orderdatas,'item_data': item_data,}

    return render(request, 'procurement/request_order.html', context)

def request_order_add(request):
    if request.method=="POST":
        order = Order.objects.create()

        citem_name=request.POST.get('item_name')
        citem_type=request.POST.get('item_type')
        cquantity=request.POST.get('quantity')

        # Add requested_date to the order object
        order.requested_date = datetime.now().date()
        order.request_approved = 'Pending'
        order.purchase_approved = 'Pending'
        order.inventory_approved = 'Pending'
        order.save()

        query = OrderHasItem.objects.create(order=order, item_id=citem_name, type=citem_type,quantity=cquantity)
        query.save()
        messages.info(request, "Order Request Added Successfully!")
        return redirect("/request_order")
    
        
    item_data = Item.objects.all()
    context = {
        'data1': item_data,
    }

    return render(request, 'procurement/request_order_add.html', context)

def request_order_edit(request,order_id):
    edit = OrderHasItem.objects.get(order_id=order_id)
    
    if request.method == "POST":
        citem_name=request.POST.get('item_name')
        citem_type=request.POST.get('item_type')
        cquantity=request.POST.get('quantity')
        
        # Update the attributes
        edit.item_id = citem_name
        edit.type = citem_type
        edit.quantity = cquantity
        
        # Save the changes
        edit.save()
        messages.warning(request, "Request Updated Successfully!")
        # Optionally, redirect to a success page or another view
        return redirect("/request_order")

    d = OrderHasItem.objects.get(order_id=order_id)
    data1 = Item.objects.all()
    context = {"d": d, "item": edit, "data1": data1}

    return render(request, 'procurement/request_order_edit.html', context)


def request_order_delete(request, order_id):
    try:
        order_item = OrderHasItem.objects.get(order_id=order_id)
        order = order_item.order
        order_item.delete()

        # Check if there are any remaining items associated with this order
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
        order.save()
        return JsonResponse({'message': 'Order request approved successfully.'})
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found.'}, status=404)

def reject_request(request, order_id):
    try:
        order = Order.objects.get(pk=order_id)
        order.request_approved = 'Rejected'
        order.save()
        return JsonResponse({'message': 'Order request rejected successfully.'})
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found.'}, status=404)

def rfq(request):
    data = OrderHasItemSupplier.objects.all()
    context = {"data1":data}

    return render(request, 'procurement/rfq.html', context)

def rfq_add(request, order_id):
    if request.method == "POST":
        csupplier_name = request.POST.get('supplier_name')
        citem_id = request.POST.get('item_id')
        cprice = request.POST.get('price')

        # Save the RFQ
        query = OrderHasItemSupplier.objects.create(supplier_id=csupplier_name, item_id=citem_id, order_id=order_id, price=cprice, status='pending')
        messages.info(request, "RFQ Added Successfully!")
        return redirect("/rfq")

    # Get orders and items with request_approved = 'approved'
    order_data = OrderHasItem.objects.filter(order__request_approved='approved')
    supplier_data = Supplier.objects.all()
    existing_rfq = OrderHasItemSupplier.objects.filter(order_id=order_id)
    
    context = {
        'data1': order_data,
        'data2' : supplier_data,
        'existing_rfq' : existing_rfq,
        'order_id': order_id,
    }

    return render(request, 'procurement/rfq_add.html', context)

def rfq_edit(request,id):
    edit = OrderHasItemSupplier.objects.get(id=id)
    
    if request.method == "POST":
        csupplier_name=request.POST.get('supplier_name')
        citem_id=request.POST.get('item_id')
        cprice=request.POST.get('price')
        
        # Update the attributes
        edit.supplier_id = csupplier_name
        edit.item_id = citem_id
        edit.price = cprice
        
        # Save the changes
        edit.save()
        messages.warning(request, "RFQ Updated Successfully!")
        # Optionally, redirect to a success page or another view
        return redirect("/rfq")

    d = OrderHasItemSupplier.objects.get(id=id)
    order_data = OrderHasItem.objects.filter(order__request_approved='approved')
    supplier_data = Supplier.objects.all()
    
    context = {
        'data1': order_data,
        'data2' : supplier_data,
        'd': d,
    }

    return render(request, 'procurement/rfq_edit.html', context)

def rfq_delete(request, id):
    d = OrderHasItemSupplier.objects.get(id=id)
    d.delete()
    messages.error(request, "RFQ Deleted Successfully!")
    return redirect("/rfq")

def approve_rfq(request, id):
    try:
        order = OrderHasItemSupplier.objects.get(pk=id)
        order.status = 'Approved'
        order.save()
        return JsonResponse({'message': 'Purchase approved successfully.'})
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found.'}, status=404)

def reject_rfq(request, id):
    try:
        order = OrderHasItemSupplier.objects.get(pk=id)
        order.status = 'Rejected'
        order.save()
        return JsonResponse({'message': 'Purchase rejected successfully.'})
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found.'}, status=404)

def purchase_order(request):
    approved_supp = OrderHasItemSupplier.objects.filter(status='approved').values('supplier_id', 'order_id', 'item_id', 'price', 'status', 'modified_date').distinct()
    item_data = Item.objects.all()
    supplier_data = Supplier.objects.all()
    
    context = {"approved_supp": approved_supp, 'item_data': item_data, 'supplier_data': supplier_data,}

    return render(request, 'procurement/purchase_order.html', context)

def generate_purchase_order(request, supplier_id):
    data = OrderHasItemSupplier.objects.filter(supplier_id=supplier_id, status='approved')
    item_data = Item.objects.all()
    qty_data = OrderHasItem.objects.all()
    supplier_data = Supplier.objects.all()
    
    context = {
        'data': data,
        'item_data': item_data, 
        'qty_data': qty_data,
        'supplier_data': supplier_data,
    }

    return render(request, 'procurement/generate_purchase_order.html', context)











 







