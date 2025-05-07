from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

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

        email = self.normalize_email(email)

        try:
            emp_instance = Employee.objects.get(emp_no=emp_no)
        except Employee.DoesNotExist:
            raise ValueError("유효하지 않은 직번입니다.")

        user = self.model(
            userID=userID,
            email=email,
            emp_no=emp_instance,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, userID, email, password=None, emp_no=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(userID, email, password, emp_no, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    emp_no = models.ForeignKey(Employee, to_field='emp_no', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=30, blank=True)
    userID = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    position = models.CharField(max_length=20, blank=True)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'userID'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.userID} ({self.emp_no.emp_no if self.emp_no else 'No Emp'})"

    def save(self, *args, **kwargs):
        if self.emp_no:
            self.name = self.emp_no.name
            self.position = self.emp_no.position
        super().save(*args, **kwargs)
