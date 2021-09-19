from django.contrib import auth
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from .models import User
from .methods import nusnet_id_exists, student_number_exists
from common.constants import (
    MESSAGE, USERNAME, EMAIL, PASSWORD, REFRESH, ACCESS, TOKENS, TELEGRAM_HANDLE, STUDENT_NUMBER, NUSNET_ID
) 

class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=50, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = [USERNAME, EMAIL, PASSWORD, STUDENT_NUMBER, NUSNET_ID, TELEGRAM_HANDLE]

    def validate(self, attrs):
        # Check if student number and nusnet id already exist
        nusnet_id = attrs.get(NUSNET_ID).lower()
        student_number = attrs.get(STUDENT_NUMBER).upper()

        if nusnet_id_exists(nusnet_id):
            raise ValidationError(detail="User with this NUSNET id already exists.")

        if student_number_exists(student_number):
            raise ValidationError(detail="User with this student number already exists.")


        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=255, min_length=8, write_only=True)
    username = serializers.CharField(
        max_length=255, min_length=3, read_only=True)

    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj[EMAIL])

        return {
            REFRESH: user.tokens()[REFRESH],
            ACCESS: user.tokens()[ACCESS]
        }

    class Meta:
        model = User
        fields = [EMAIL, PASSWORD, USERNAME, TOKENS]

    def validate(self, attrs):
        email = attrs.get(EMAIL, '')
        password = attrs.get(PASSWORD, '')
        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed({MESSAGE:'Invalid credentials, please try again.'})
        if not user.is_active:
            raise AuthenticationFailed({MESSAGE:'Account disabled, please contact admin.'})
        if not user.is_verified:
            raise AuthenticationFailed({MESSAGE:'Email is not verified.'})

        return {
            EMAIL: user.email,
            USERNAME: user.username,
            TOKENS: user.tokens()
        }


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [USERNAME, EMAIL, STUDENT_NUMBER, NUSNET_ID, TELEGRAM_HANDLE]