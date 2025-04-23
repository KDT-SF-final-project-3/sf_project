from django.contrib import admin
from django.contrib.auth.admin import UserAdmin # 기본 User 모델을 관리하는 관리자 클래스
from .models import CustomUser # 직접 만든 사용자 모델 가져오기

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('emp_no', 'name', 'userID', 'email', 'position', 'is_approved', 'is_staff')
    list_filter = ('is_approved', 'position', 'is_staff')

    # 필드 그룹화
    fieldsets = (
        (None, {'fields': ('emp_no', 'name', 'userID', 'email', 'password', 'position')}),
        ('Permissions', {'fields': ('is_approved', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    # 새 유저 추가할때 필드
    add_fieldsets = (
        (None, {
            'classes': ('wide',), # 유저 등록 폼의 입력창 너비를 넓게
            'fields': ('emp_no', 'name', 'userID', 'email', 'position', 'password1', 'password2', 'is_approved', 'is_staff', 'is_superuser'),
        }),
    )
    search_fields = ('userID', 'emp_no', 'name')
    ordering = ('emp_no',)

admin.site.register(CustomUser, CustomUserAdmin)
