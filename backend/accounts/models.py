from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
from .managers import CustomUserManager

# 직원 모델
class Employee(models.Model):
    emp_no = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=30)
    team = models.CharField(max_length=20)
    position = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.emp_no} - {self.name} ({self.position})"


# 사용자 모델
class CustomUser(AbstractBaseUser):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, null=True)
    userID = models.CharField(max_length=30, unique=True)  # 로그인용 ID
    email = models.EmailField(unique=True)
    is_approved = models.BooleanField(default=False)  # 승인 여부
    is_active = models.BooleanField(default=True) # 계정 활성화 여부
    is_staff = models.BooleanField(default=False) # 관리자 여부
    last_login = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'userID'
    REQUIRED_FIELDS = ['employee', 'email']

    objects = CustomUserManager()

    # 직원 이름을 가져오는 프로퍼티
    @property
    def name(self):
        return self.employee.name  # 직원 모델에서 이름 가져옴

    # 직원 직책을 가져오는 프로퍼티
    @property
    def position(self):
        return self.employee.position  # 직원 모델에서 직책 가져옴

    def save(self, *args, **kwargs):
        if self.is_authenticated:  # 인증된 유저일 경우
            self.last_login = timezone.now()  # 로그인 시 last_login을 현재 시간으로 설정
        super().save(*args, **kwargs)  # 부모 클래스의 save 호출

    def __str__(self):
        return f"{self.userID} ({self.employee.emp_no})"