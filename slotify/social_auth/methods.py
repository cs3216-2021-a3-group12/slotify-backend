import os
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from google.auth.transport import requests
from google.oauth2 import id_token
from authentication.models import User
from authentication.methods import get_user_by_email
from common.constants import EMAIL, USERNAME, TOKENS

class Google:
    """Google class to fetch the user info and return it"""
    @staticmethod
    def validate(auth_token):
        """
        validate method Queries the Google oAUTH2 api to fetch the user info
        """
        try:
            idinfo = id_token.verify_oauth2_token(auth_token, requests.Request())

            if 'accounts.google.com' in idinfo['iss']:
                return idinfo

        except:
            return "The token is either invalid or has expired"


def register_social_user(provider, user_id, email, name):
    filtered_user_by_email = get_user_by_email(email=email)

    # If user exists, check if provider is the same
    if filtered_user_by_email:
        if provider != filtered_user_by_email.auth_provider:
            raise AuthenticationFailed(
                detail= f"Please continue your login using {filtered_user_by_email.auth_provider.capitalize()}")

    else:
        new_user = User(
            username=name,
            email=email,
            auth_provider=provider,
            is_verified=True
        )

        new_user.set_password(settings.SECRET_KEY)
        # new_user.is_verified = True
        # new_user.auth_provider = provider
        new_user.save()

    authenticated_user = authenticate(email=email, password=settings.SECRET_KEY)

    return {
        EMAIL: authenticated_user.email,
        USERNAME: authenticated_user.username,
        TOKENS: authenticated_user.tokens()
    }