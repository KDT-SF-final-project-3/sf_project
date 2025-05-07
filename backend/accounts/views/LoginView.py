from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class LoginView(APIView):
    def post(self, request):
        userID = request.data.get('userID')
        password = request.data.get('password')

        if not userID or not password:
            return Response({'error': 'ID와 비밀번호를 모두 입력하세요.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=userID, password=password)

        if user is not None:
            if not user.is_active:
                return Response({'error': '비활성화된 계정입니다.'}, status=status.HTTP_403_FORBIDDEN)

            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh_token': str(refresh),
                'access_token': str(refresh.access_token),
                'userID': user.userID,
                'email': user.email,
                'is_approved': user.is_approved,  # ✅ 이 줄 추가!
                'name': user.name,
            }, status=status.HTTP_200_OK)

        return Response({'error': '아이디 또는 비밀번호가 올바르지 않습니다.'}, status=status.HTTP_401_UNAUTHORIZED)