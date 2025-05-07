from django.urls import path
from .views.RegisterView import RegisterView, CheckEmpNoView, CheckUserIDView
from .views.LoginView import LoginView
from rest_framework_simplejwt.views import (
    TokenObtainPairView, # Access Token, Refresh Token 발급
    TokenRefreshView, # Access Token이 만료되면 Refresh Token을 보내서 새로 발급해줌
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('check-emp-no/', CheckEmpNoView.as_view(), name='check_emp_no'),
    path('check-user-id/', CheckUserIDView.as_view(), name='check_user_id'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]