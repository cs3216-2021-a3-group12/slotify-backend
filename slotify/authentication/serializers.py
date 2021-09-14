from django.contrib import auth
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from .models import User
from common.constants import MESSAGE, USERNAME, EMAIL, PASSWORD, REFRESH, ACCESS, TOKENS

class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=50, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = [USERNAME, EMAIL, PASSWORD]

    def validate(self, attrs):
        # TODO: handle validation here
        email = attrs.get(EMAIL, '')
        username = attrs.get(USERNAME, '')
        password = attrs.get(PASSWORD, '')

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
        fields = [EMAIL, PASSWORD, USERNAME, 'tokens']

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