import rest_framework_simplejwt
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail.message import EmailMessage
from .serializers import SignupSerializer, LoginSerializer

User = get_user_model()
class SignupView(CreateAPIView):
    model = User
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        response = super(SignupView, self).create(request, *args, **kwargs)
        data = {
            "data": response.data,
            "message": {
                "msg": "You have successfully created the account.",
                "status": "ACCOUNT_CREATE_OK"
            }
        }

        response.data = data
        return response



class LoginView(APIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            return JsonResponse(serializer.validated_data, status=status.HTTP_200_OK)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data["refresh_token"]

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return JsonResponse({"message": "성공적으로 로그아웃 되었습니다."}, status=status.HTTP_200_OK)

        except(rest_framework_simplejwt.exceptions.TokenError):
            return JsonResponse({"message": "refresh_token이 유효하지 않거나 만료되었습니다."}, status=status.HTTP_401_UNAUTHORIZED)