from rest_framework import serializers
from .models import CustomUser, Employee
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)  # 비밀번호 확인

    class Meta:
        model = CustomUser
        fields = ('emp_no', 'name', 'userID', 'password', 'password2', 'email', 'position')
        extra_kwargs = {'password': {'write_only': True},
                        'password2': {'write_only': True},
                        'name': {'read_only': True},  # create 메서드에서 Employee 정보로 채워지므로 읽기 전용
                        'position': {'read_only': True}  # create 메서드에서 Employee 정보로 채워지므로 읽기 전용
        }

    def validate_emp_no(self, value):
        # 1. Employee 테이블에서 직번 존재 여부 확인
        if not Employee.objects.filter(emp_no=value).exists():
            raise ValidationError("존재하지 않는 직번입니다.")

        # 2. CustomUser 테이블에서 동일한 직번이 사용되고 있는지 확인
        if CustomUser.objects.filter(emp_no=value).exists():
            raise ValidationError("이 직번은 이미 사용 중입니다.")

        return value

    def validate_userID(self, value):
        # userID 중복 체크
        if CustomUser.objects.filter(userID=value).exists():
            raise ValidationError("이미 존재하는 아이디입니다.")
        return value

    def validate(self, data):
        # 비밀번호 확인
        if data['password'] != data['password2']:
            raise ValidationError("비밀번호가 다릅니다.")
        return data

    def create(self, validated_data):
        emp_no_value = validated_data.pop('emp_no')  # emp_no를 먼저 가져옴
        validated_data.pop('password2')

        try:
            employee = Employee.objects.get(emp_no=emp_no_value)
            print(f"Found employee in create - emp_no: '{employee.emp_no}'")
        except Employee.DoesNotExist:
            print(f"Employee NOT found in create with emp_no: '{emp_no_value}'")
            raise ValidationError("해당 직번의 직원 정보가 존재하지 않습니다.")

        user = CustomUser.objects.create_user(
            userID=validated_data['userID'],
            password=validated_data['password'],
            email=validated_data['email'],
            emp_no=emp_no_value,  # CharField 이므로 문자열 직번 저장
            name=employee.name,
            position=employee.position
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