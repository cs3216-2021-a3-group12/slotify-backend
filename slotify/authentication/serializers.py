from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=50, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        password = attrs.get('password', '')

        # if not name.isalnum():
        #     raise serializers.ValidationError("Name should consist of alphanumeric characters only.")

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)