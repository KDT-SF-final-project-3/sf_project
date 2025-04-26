from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import SensorData
from .serializers import SensorDataSerializer

@api_view(['POST'])
def sensor_data(request):
    serializer = SensorDataSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'status': 'success', 'data': serializer.data})
    return Response({'status': 'error', 'errors': serializer.errors})