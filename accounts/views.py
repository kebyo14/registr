from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import RegisterSerializer, LoginSerializer, VerifyOTPSerializer
from .models import OTP
from .utils import send_otp_email
from django.contrib.auth import login, logout

from django.core.mail import send_mail

def send_otp_email(user, code):
    send_mail(
        subject='Ваш код подтверждения',
        message=f'Ваш OTP-код: {code}',
        from_email='noreply@example.com',
        recipient_list=[user.email],
        fail_silently=False,
    )
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            otp = OTP.objects.filter(user=user).latest('created_at')
            send_otp_email(user, otp.code)
            return Response({"message": "Регистрация прошла успешно. Проверьте email."}, status=201)
        return Response(serializer.errors, status=400)

class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "Пользователь подтвержден"})
        return Response(serializer.errors, status=400)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(email=serializer.validated_data['email'])
            login(request, user)
            return Response({"message": "Вы вошли в систему"})
        return Response(serializer.errors, status=400)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Вы вышли из системы"})
