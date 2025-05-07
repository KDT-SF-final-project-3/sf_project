from rest_framework import serializers
from .models import CustomUser, Employee
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('emp_no', 'name', 'userID', 'password', 'password2', 'email', 'position')
        extra_kwargs = {
            'password': {'write_only': True},
            'password2': {'write_only': True},
            'name': {'read_only': True},         # 서버에서 자동으로 입력됨
            'position': {'read_only': True}      # 서버에서 자동으로 입력됨
        }

    def validate_emp_no(self, value):        
        if not Employee.objects.filter(emp_no=value).exists():
            raise ValidationError("존재하지 않는 직번입니다.")
        if CustomUser.objects.filter(emp_no__emp_no=value).exists():
            raise ValidationError("이 직번은 이미 사용 중입니다.")
        return value

    def validate_userID(self, value):
        if CustomUser.objects.filter(userID=value).exists():
            raise ValidationError("이미 존재하는 아이디입니다.")
        return value

    def validate(self, data):
        if data['password'] != data['password2']:
            raise ValidationError("비밀번호가 다릅니다.")
        return data

    def create(self, validated_data):
        emp_no = validated_data['emp_no']
        validated_data.pop('password2')

        # employee 객체를 가져옴
        employee = Employee.objects.get(emp_no=emp_no)

        # CustomUser 생성
        user = CustomUser.objects.create_user(
            userID=validated_data['userID'],
            password=validated_data['password'],
            email=validated_data['email'],
            emp_no=employee,
            name=employee.name,
            position=employee.position
        )
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['userID'] = user.userID
        return token

    def validate(self, attrs):
        attrs['username'] = attrs.get('userID')
        data = super().validate(attrs)
        return data