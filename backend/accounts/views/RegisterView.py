from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import UserRegisterSerializer
from ..models import Employee, CustomUser

class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "회원가입 완료"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CheckEmpNoView(APIView):
    def post(self, request):
        emp_no = request.data.get('emp_no')
        if not emp_no:
            return Response({"error": "직번을 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)
        is_employee = Employee.objects.filter(emp_no=emp_no).exists()
        is_used = CustomUser.objects.filter(emp_no=emp_no).exists()
        if not is_employee:
            return Response({"message": "직원이 아닙니다."}, status=status.HTTP_200_OK)
        if is_used:
            return Response({"message": "이미 사용 중인 직번입니다."}, status=status.HTTP_200_OK)
        return Response({"message": "직원입니다."}, status=status.HTTP_200_OK)

class CheckUserIDView(APIView):
    def post(self, request):
        userID = request.data.get('userID')
        if not userID:
            return Response({"error": "아이디를 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)
        is_exists = CustomUser.objects.filter(userID=userID).exists()
        if is_exists:
            return Response({"message": "이미 존재하는 ID입니다."}, status=status.HTTP_200_OK)
        return Response({"message": "가입할 수 있는 ID입니다."}, status=status.HTTP_200_OK)