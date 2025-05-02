from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from ..models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken

class LoginView(APIView):
    def post(self, request):
        # 요청에서 userID와 password 받기
        userID = request.data.get('userID')
        password = request.data.get('password')
        
        try:
            # userID로 사용자 찾기
            user = CustomUser.objects.filter(userID=userID).first()
        except CustomUser.DoesNotExist:
            return Response({"detail": "사용자를 찾을 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
    
        if user and user.is_approved:
            if user.check_password(password):
                # 로그인 성공 후 토큰 생성
                refresh = RefreshToken.for_user(user)

                return Response({
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                    'is_approved': user.is_approved,  # 승인 여부
                    'name' : user.name # 사용자 이름
                }, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "잘못된 비밀번호입니다."}, status=status.HTTP_400_BAD_REQUEST)
        elif user and not user.is_approved:
            return Response({"detail": "사용자가 승인되지 않았습니다."}, status=status.HTTP_403_FORBIDDEN)