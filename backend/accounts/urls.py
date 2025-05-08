# accounts/urls.py

from django.urls import path
from .views.RegisterView import RegisterView, CheckEmpNoView, CheckUserIDView

from .views.SimpleLoginView import SimpleLoginView



urlpatterns = [
    # 회원가입 관련
    path('register/', RegisterView.as_view(), name='register'),
    path('check-emp-no/', CheckEmpNoView.as_view(), name='check_emp_no'),
    path('check-user-id/', CheckUserIDView.as_view(), name='check_user_id'),

    # 로그인 관련
    # path('login/', LoginView.as_view(), name='login'), 
    path('login/', SimpleLoginView.as_view(), name='login'), 


    # JWT 토큰 관련 URL은 루트 urls.py로 이동 (중복 제거)

]