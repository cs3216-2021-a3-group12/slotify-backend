from django.shortcuts import render
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import generics, serializers,status
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.response import Response
from .models import User
from .util import RegistrationUtil
from common.constants import MESSAGE, TOKEN

import jwt

# Create your views here.
class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        
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