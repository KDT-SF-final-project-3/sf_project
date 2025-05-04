# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Table3View
from .serializers import Table3Serializer

class Table3APIView(APIView):
    def get(self, request):
        data = Table3View.objects.all().order_by('-id')
        serializer = Table3Serializer(data, many=True)
        return Response(serializer.data)
    



from rest_framework.generics import ListAPIView
from .models import Table4
from .serializers import Table4Serializer

class Table4APIView(ListAPIView):
    queryset = Table4.objects.all().order_by('-id')  # 최신순 정렬 가능
    serializer_class = Table4Serializer



from .models import Table7
from .serializers import Table7Serializer

class Table7APIView(APIView):
    def get(self, request):
        row = Table7.objects.first()  # 가장 첫 번째 1행만 가져옴
        if row:
            serializer = Table7Serializer(row)
            return Response(serializer.data)
        else:
            return Response({}, status=204)
        

from rest_framework.views import APIView
from django.http import HttpResponse
import csv
from .models import Table3View  # 기존의 Table3View 사용
from datetime import datetime
from .models import Table4, Table5

def export_table4_csv(request):
    now_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"table4_export_{now_str}.csv"

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    response.write('\ufeff')  # BOM

    writer = csv.writer(response)
    writer.writerow(['ID', '명령어', '시작 시간', '종료 시간'])

    for item in Table4.objects.all().order_by('-id'):
        writer.writerow([item.id, item.command, item.start_time, item.end_time])

    return response


def export_table5_csv(request):
    now_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"table5_export_{now_str}.csv"

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    response.write('\ufeff')

    writer = csv.writer(response)
    writer.writerow(['ID', '명령어', '시작 시간', '종료 시간'])

    for item in Table5.objects.all().order_by('-id'):
        writer.writerow([item.id, item.command, item.start_time, item.end_time])

    return response
class Table3ExportAPIView(APIView):
    def get(self, request):
        start = request.GET.get('start')
        end = request.GET.get('end')

        if not (start and end):
            return Response({'error': 'start와 end 쿼리 파라미터가 필요합니다.'}, status=400)

        queryset = Table3View.objects.filter(timestamp__range=[start, end]).order_by('timestamp')

        # ✅ 현재 시각을 파일 이름에 추가
        now_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"table3_export_{now_str}.csv"

        # ✅ BOM 추가 + 동적 파일 이름 지정
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        response.write('\ufeff')  # 한글 인코딩 깨짐 방지용 BOM

        writer = csv.writer(response)
        writer.writerow(['ID', '조도', '온도', '습도', '팬 상태', 'LED 상태', '시간'])

        for item in queryset:
            writer.writerow([
                item.id,
                item.light,
                item.temperature,
                item.humidity,
                item.fan_status,
                item.led_status,
                str(item.timestamp)
            ])

        return response
    
    
from django.http import JsonResponse
from .models import Table5

def table5(request):
    data = list(Table5.objects.order_by('-id').values())  # 최신순
    return JsonResponse({'items': data})  # React 대응 구조