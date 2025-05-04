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
    path('table5/', views.table5),  # ✅ 여기서 처리
    path('table4/export/', views.export_table4_csv),
    path('table5/export/', views.export_table5_csv),
]