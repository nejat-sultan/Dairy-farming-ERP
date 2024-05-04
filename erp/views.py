import os
from django.shortcuts import get_object_or_404, render,redirect
from django.core.files.storage import FileSystemStorage


from testproject import settings
from .models import CattlePhoto, CattleStatus, ContactType, Dashboard, GuaranteeType, PersonTitle, PersonType, Region, SaleType, SupplierType
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
    # data = Cattle.objects.all()
    # data = get_object_or_404(Cattle, cattle_id=cattle_id)
    # context = {"data":data}

    # return render(request, 'cattle/cattle_view.html', context)



    cattle = get_object_or_404(Cattle, cattle_id=cattle_id)
    photos = CattlePhoto.objects.filter(cattle=cattle)
    print(photos) 

    context = {
        'cattle': cattle,
        'photos': photos
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
    
    # data = CattleStatus.objects.all()
    # context = {'data1': data}

    # data = Cattle.objects.all()
    # context = {'data2': data}

    data = CattleStatus.objects.all()
    cattle_data = Cattle.objects.all()

    context = {
        'data1': data,
        'data2': cattle_data,
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
    # Pass the cattle object and cattle statuses to the template context
    context = {"cattle": edit, "cattle_statuses": cattle_statuses}

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

        # Create a new CattlePhoto instance
        # photo = CattlePhoto.objects.create(
        #     cattle_id=cattle_id,
        #     cattle_photo_url=photo_url,
        #     cattle_photo_description=photo_description
        # )

        # messages.info(request, "Cattle Photo Added Successfully!")
        # return redirect("/cattle")
    
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
        cid=request.POST.get('id')
        cstatus=request.POST.get('status')

        query = CattleStatus(cattle_status_id=cid, cattle_status=cstatus)
        query.save()
        messages.info(request, "Cattle Status Added Successfully!")
        return redirect("/cattle_status")

    return render(request, 'cattle/cattle_status_add.html')

def cattle_status_edit(request,cattle_status_id):
    # Fetch the cattle object by its id
    edit = CattleStatus.objects.get(cattle_status_id=cattle_status_id)
    
    if request.method == "POST":
        cid=request.POST.get('id')
        cstatus=request.POST.get('status')
        
        # Update the attributes
        edit.cattle_status_id = cid
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

def supplier_type(request):
    data = SupplierType.objects.all()
    context = {"data1":data}

    return render(request, 'sales/supplier_type.html', context)

def supplier_type_add(request):
    if request.method=="POST":
        csupplier_type=request.POST.get('supplier_type')

        query = SupplierType(supplier_type=csupplier_type)
        query.save()
        messages.info(request, "Supplier Type Added Successfully!")
        return redirect("/supplier_type")

    return render(request, 'sales/supplier_type_add.html')

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

    return render(request, 'sales/supplier_type_edit.html', context)

def supplier_type_delete(request, supplier_type_id):
    d = SupplierType.objects.get(supplier_type_id=supplier_type_id)
    d.delete()
    messages.error(request, "Supplier Type Deleted Successfully!")
    return redirect("/supplier_type")


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












def request_order(request):
    return render(request, 'request_order.html')

def add_orderRequest(request):
    return render(request, 'add_orderRequest.html')


