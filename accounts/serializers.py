from rest_framework import serializers
from .models import User, OTP
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        OTP.objects.create(user=user)  # создаем OTP
        return user

class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
            otp = OTP.objects.filter(user=user).latest('created_at')
            if otp.code != data['code']:
                raise serializers.ValidationError("Неверный OTP")
            user.is_verified = True
            user.save()
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден")
        return data

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Неверные данные")
        if not user.is_verified:
            raise serializers.ValidationError("Пользователь не подтвержден")
        return data
from rest_framework import serializers
from django.contrib.auth import get_user_model
import re

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("Пароль должен быть не менее 6 символов.")
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Пароль должен содержать хотя бы одну заглавную букву.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
