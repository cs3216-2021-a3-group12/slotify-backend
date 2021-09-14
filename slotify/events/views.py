from django import http
from authentication.middleware import check_requester_is_authenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from authentication.models import User
from authentication.middleware import check_requester_is_authenticated


# Create your views here.
class EventsView(APIView):
    @check_requester_is_authenticated()
    # TODO: make sure that user is group admin
    def post(self, request, requester: User):
        return Response({"username": requester.username}, status=status.HTTP_201_CREATED)