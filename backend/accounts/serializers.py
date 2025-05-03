# 모델데이터 JSON 변경, 모델 객체로 저장
from rest_framework import serializers
from .models import CustomUser, Employee
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed


# 모델 기반 자동 필드 생성
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('emp_no', 'userID', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_emp_no(self, value):
        if not Employee.objects.filter(emp_no=value).exists():
            raise serializers.ValidationError("존재하지 않는 직번입니다.")
        return value

    def validate_userID(self, value):
        if CustomUser.objects.filter(userID=value).exists():
            raise serializers.ValidationError("이미 존재하는 아이디입니다.")
        return value

    # 자동 암호화 처리 -> 유저 생성, DB 저장, 객체 리턴 
    def create(self, validated_data):
        emp_no = validated_data['emp_no']
        employee = Employee.objects.get(emp_no=emp_no)

        # 이름과 직책은 직원 테이블에서 가져옴
        name = employee.name
        position = employee.position

        user = CustomUser.objects.create_user(
            emp_no=emp_no,
            name=name,
            userID=validated_data['userID'],
            password=validated_data['password'],
            email=validated_data['email'],
            position=position
        )
        return user
    
# SimpleJWT 기본 토큰 로직 커스터마이징
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # 필요한 경우 여기에 사용자 정보 추가 가능
        token['userID'] = user.userID
        return token

    def validate(self, attrs):
        # username 대신 userID 사용
        attrs['username'] = attrs.get('userID')
        data = super().validate(attrs)

        # if not self.user.is_approved:
        #     raise AuthenticationFailed("관리자 승인 후 로그인할 수 있습니다.")

        return data