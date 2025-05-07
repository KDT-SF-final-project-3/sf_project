# accounts/urls.py

from django.urls import path
from .views.RegisterView import RegisterView, CheckEmpNoView, CheckUserIDView
from .views.LoginView import LoginView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # 회원가입 관련
    path('register/', RegisterView.as_view(), name='register'),
    path('check-emp-no/', CheckEmpNoView.as_view(), name='check_emp_no'),
    path('check-user-id/', CheckUserIDView.as_view(), name='check_user_id'),

    # 로그인 관련
    path('login/', LoginView.as_view(), name='login'),  # ✅ 정상 경로만 유지

    # JWT 토큰
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),

]