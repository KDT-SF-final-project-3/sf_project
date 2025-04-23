from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from .managers import CustomUserManager

# 사용자 모델
class CustomUser(AbstractBaseUser, PermissionsMixin):
    emp_no = models.CharField(max_length=10, unique=True)  # 직번
    name = models.CharField(max_length=30)
    userID = models.CharField(max_length=30, unique=True)  # 로그인용 ID
    email = models.EmailField(unique=True)
    position = models.CharField(max_length=20)
    is_approved = models.BooleanField(default=False)  # 승인 여부
    is_active = models.BooleanField(default=True) # 계정 활성화 여부
    is_staff = models.BooleanField(default=False) # 관리자 여부

    # groups 필드 수정 (related_name 추가)
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_groups',  # 새 이름 지정
        blank=True,
    )

    # user_permissions 필드 수정 (related_name 추가)
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions',  # 새 이름 지정
        blank=True,
    )

    USERNAME_FIELD = 'userID'
    REQUIRED_FIELDS = ['emp_no', 'name', 'email',  'position']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.userID} ({self.emp_no})"