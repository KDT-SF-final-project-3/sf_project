# 모델데이터 JSON 변경, 모델 객체로 저장
from rest_framework import serializers
from .models import CustomUser

# 모델 기반 자동 필드 생성
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('emp_no', 'name', 'userID', 'password', 'email', 'position')
        extra_kwargs = {'password': {'write_only': True}}

    # 자동 암호화 처리 -> 유저 생성, DB 저장, 객체 리턴 
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user