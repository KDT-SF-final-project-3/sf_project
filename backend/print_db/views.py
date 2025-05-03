from django.http import JsonResponse
from .models import Table1, Table2, Table3, Table4

def get_tables(request):
    data = {
        'table1': list(Table1.objects.values()),
        'table2': list(Table2.objects.values()),
        'table3': list(Table3.objects.values()),
        'table4': list(Table4.objects.values()),
    }
    return JsonResponse(data, safe=False)