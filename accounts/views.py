from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import RegisterSerializer, LoginSerializer, VerifyOTPSerializer
from .models import OTP
from django.contrib.auth import login, logout, get_user_model
from django.core.mail import send_mail
from drf_yasg.utils import swagger_auto_schema

User = get_user_model()


def send_otp_email(user, code):
    send_mail(
        subject='Ваш код подтверждения',
        message=f'Ваш OTP-код: {code}',
        from_email='noreply@example.com',
        recipient_list=[user.email],
        fail_silently=False,
    )


class RegisterView(APIView):
    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            otp = OTP.objects.filter(user=user).latest('created_at')
            send_otp_email(user, otp.code)
            return Response({"message": "Регистрация прошла успешно. Проверьте email."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    @swagger_auto_schema(request_body=VerifyOTPSerializer)
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "Пользователь подтвержден"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(email=serializer.validated_data['email'])
            login(request, user)
            return Response({"message": "Вы вошли в систему"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema()
    def post(self, request):
        logout(request)
        return Response({"message": "Вы вышли из системы"})
