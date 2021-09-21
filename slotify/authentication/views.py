from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import generics, status
from rest_framework.views import APIView
from .serializers import RegisterSerializer, LoginSerializer, UserProfileSerializer
from rest_framework.response import Response
from .models import User, Profile
from .util import RegistrationUtil
from .middleware import check_requester_is_authenticated
from .methods import (
    check_if_other_user_with_field_exists, user_to_json, get_user_with_student_number, get_user_with_nusnet_id
)
from common.constants import MESSAGE, TOKEN, NUSNET_ID, STUDENT_NUMBER, TELEGRAM_HANDLE, PROFILE, USERNAME, EMAIL

import jwt

FIELDS_TO_CHECK =  {
    NUSNET_ID: get_user_with_nusnet_id,
    STUDENT_NUMBER: get_user_with_student_number
}

# Create your views here.
class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        user = User.objects.get(email=user_data[EMAIL])
        
        current_site = get_current_site(request)
        domain = current_site.domain

        RegistrationUtil.send_email_verification(user, domain)

        return Response(user_data, status=status.HTTP_201_CREATED)

class VerifyEmailView(generics.GenericAPIView):
    def get(self, request):
        token = request.GET.get(TOKEN)

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response({MESSAGE: "Successfully verified email."}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            # TODO: provide an API to handle this case
            return Response({MESSAGE: "Verification link expired."}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({MESSAGE: "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({MESSAGE: "Some error occurred. Please try again later"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception = True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class UserProfileView(APIView):
    @check_requester_is_authenticated
    def get(self, request, requester):
        return Response(user_to_json(requester), status=status.HTTP_200_OK)

    @check_requester_is_authenticated
    def patch(self, request, requester):
        serializer = UserProfileSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        # check if nusnet id already exists (but does not belong to requester)
        for field, fetch_user_by_field_function in FIELDS_TO_CHECK.items():
            if not check_if_other_user_with_field_exists(
                fetch_user_by_field_function, validated_data[field], requester
            ):
                continue

            data = {
                MESSAGE: f"Failed to update {field} as it is already registered by another user."
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        # check if requester has profile already
        if not hasattr(requester, PROFILE):            
            profile = Profile(
                user=requester,
                student_number=validated_data[STUDENT_NUMBER],
                telegram_handle=validated_data[TELEGRAM_HANDLE],
                nusnet_id=validated_data[NUSNET_ID]
            )
            profile.save()
            data = user_to_json(requester)

            return Response(data, status=status.HTTP_200_OK)
        try: 
            requester.username = validated_data[USERNAME]
            requester.save()

            # validated_data.pop(USERNAME, None)

            requester.profile.__dict__.update(validated_data)
            requester.profile.save()
        except:
            data = {
                MESSAGE: "An error occurred, please try again later"
            }
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        data = user_to_json(requester)

        return Response(data, status=status.HTTP_200_OK)
    
    