from datetime import timedelta
from django.utils import timezone
from .models import Cattle, CattleHasVaccine, Stock
from django.db.models import ExpressionWrapper, FloatField, F
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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


def get_overdue_vaccines():
    overdue_cattle = []
    all_cattle = Cattle.objects.all()
    one_week_ago = timezone.now() - timedelta(days=7)

    for cattle in all_cattle:
        last_vaccination = CattleHasVaccine.objects.filter(cattle=cattle).order_by('-cattle_given_time').first()
        if not last_vaccination or last_vaccination.cattle_given_time < one_week_ago:
            overdue_cattle.append({
                'name': cattle.cattle_name,
                'last_vaccination': last_vaccination.cattle_given_time if last_vaccination else 'Never'
            })

    return overdue_cattle

def get_low_quantity_items():
    low_quantity_items = Stock.objects.annotate(
        quantity_float=ExpressionWrapper(
            F('quantity'),
            output_field=FloatField()
        )
    ).filter(quantity_float__lt=5)
    return low_quantity_items