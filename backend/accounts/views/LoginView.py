from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import CustomUser
from rest_framework import status
from django.contrib.auth import login  # Django 세션 관리

class SimpleLoginView(APIView):  # 또는 LoginView
    def post(self, request):
        userID = request.data.get('userID')
        password = request.data.get('password')

        if not userID or not password:
            return Response({'error': 'ID와 비밀번호를 모두 입력하세요.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(userID=userID)
            if not user.is_approved:
                return Response({'error': '승인되지 않은 계정입니다.'}, status=status.HTTP_403_FORBIDDEN)  # 403 Forbidden 응답

            if user.check_password(password):
                login(request, user)  # Django 세션에 사용자 정보 저장
                return Response({
                    'message': f'{user.userID}님 로그인 성공 (인증 없이)',
                    'name': user.name,
                    'userID': user.userID,
                    'is_approved': user.is_approved,  # 응답에 is_approved 값 포함 (프론트엔드에서 활용 가능)
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': '비밀번호가 올바르지 않습니다 (인증 없이)'}, status=status.HTTP_401_UNAUTHORIZED)
        except CustomUser.DoesNotExist:
            return Response({'error': '해당 ID의 사용자를 찾을 수 없습니다 (인증 없이)'}, status=status.HTTP_401_UNAUTHORIZED)