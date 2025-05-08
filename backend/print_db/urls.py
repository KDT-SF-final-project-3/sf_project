from django.urls import path
from . import views


from .views import (
    Table3APIView, Table4APIView, Table7APIView,
    Table3ExportAPIView  # ← export 뷰 추가!
)

urlpatterns = [
    path('table3/', Table3APIView.as_view()),  # 기존 API
    path('table3/export/', Table3ExportAPIView.as_view()),  # ✅ 내보내기 API
    path('table4/', Table4APIView.as_view()),
    path('table7/', Table7APIView.as_view()),
    path('table4/export/', views.export_table4_csv),
    path('table5/export/', views.export_table5_csv),
    path('table5/', views.get_table5_data),  # ✅ 이 줄 추가!

    path('table4/json/', views.get_table4_data, name='get_table4_data'),
    path('table5/json/', views.get_table5_data, name='get_table5_data'),
    path('table6/', views.get_table6_data),  # ✅ 이 줄이 꼭 필요

]