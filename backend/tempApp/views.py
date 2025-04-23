from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Test

def get_data(request) :
    data = list(Test.objects.values()) # 리스트 형태로 변환
    return JsonResponse(data, safe= False)
