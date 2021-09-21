from rest_framework import serializers
from .methods import register_social_user, Google
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = Google.validate(auth_token)
        sub = user_data.get('sub', None)
        if not sub:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )

        if user_data['aud'] != settings.GOOGLE_CLIENT_ID:
            raise AuthenticationFailed('Authentication failed. Please try again.')

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'google'

        print("USER_DATA:", user_data)

        return register_social_user(
            provider=provider, user_id=user_id, email=email, name=name)