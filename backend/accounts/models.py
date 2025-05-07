from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager

# 직원 모델
class Employee(models.Model):
    emp_no = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=30)
    team = models.CharField(max_length=20)
    position = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.emp_no} - {self.name} ({self.position})"

class CustomUserManager(BaseUserManager):
        def create_user(self, userID, email, password=None, emp_no=None, **extra_fields):
            if not userID:
                raise ValueError("ID는 필수입니다.")
            if not email:
                raise ValueError("이메일은 필수입니다.")
            if not emp_no:
                raise ValueError("직번은 필수입니다.")

            try:
                employee = Employee.objects.get(emp_no=emp_no)
            except Employee.DoesNotExist:
                raise ValueError("해당 직번의 직원이 존재하지 않습니다.")

            email = self.normalize_email(email)
            user = self.model(
                userID=userID,
                email=email,
                emp_no=employee,
                name=employee.name,
                position=employee.position,
                **extra_fields
            )
            user.set_password(password)
            user.save(using=self._db)
            return user

        def create_superuser(self, userID, email, password=None, emp_no=None, **extra_fields):
            extra_fields.setdefault('is_staff', True)
            extra_fields.setdefault('is_superuser', True)
            return self.create_user(userID, email, password, emp_no, **extra_fields)
    


# 사용자 모델
class CustomUser(AbstractBaseUser):
    emp_no = models.ForeignKey(Employee, to_field='emp_no', on_delete=models.CASCADE)  # 직번
    name = models.CharField(max_length=30)    # 이름
    userID = models.CharField(max_length=30, unique=True)  # 로그인용 ID
    email = models.EmailField(unique=True)  # 이메일
    position = models.CharField(max_length=20)
    is_approved = models.BooleanField(default=False)  # 승인 여부
    is_active = models.BooleanField(default=True) # 계정 활성화 여부
    is_staff = models.BooleanField(default=False)  # 관리자 여부
    last_login = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'userID'
    REQUIRED_FIELDS = ['email', 'name']


    objects = CustomUserManager()

    def __str__(self):
        return f"{self.userID} ({self.emp_no.emp_no})"
    
    def save(self, *args, **kwargs):
        # emp_no가 설정된 경우 name과 position을 자동으로 채우기
        if self.emp_no:
            self.name = self.emp_no.name
            self.position = self.emp_no.position
        super(CustomUser, self).save(*args, **kwargs)