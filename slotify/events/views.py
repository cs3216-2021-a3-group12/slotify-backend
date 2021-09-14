from authentication.middleware import check_requester_is_authenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from authentication.models import User
from groups.models import Group
from authentication.middleware import check_requester_is_authenticated
from groups.middleware import check_group_exists, check_requester_is_group_admin

from .serializers import PostEventSerializer

# Create your views here.
class GroupEventsView(APIView):
    @check_requester_is_authenticated
    @check_group_exists
    @check_requester_is_group_admin
    def post(self, request, requester: User, group: Group):
        serializer = PostEventSerializer(data=request.data)

        return Response({"username": requester.username, "group": group.name, "category": group.category.name}, status=status.HTTP_201_CREATED)