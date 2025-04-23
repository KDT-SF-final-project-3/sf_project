# 커스텀 유저 모델 만들기 -> 사용자 관리 클래스

from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, userID, email, password=None, **extra_fields):
        if not userID:
            raise ValueError("ID is required")
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(userID=userID, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # 관리자 페이지에 접근 가능한 계정 만들기
    def create_superuser(self, userID, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(userID, email, password, **extra_fields)