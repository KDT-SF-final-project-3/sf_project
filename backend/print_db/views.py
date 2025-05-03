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