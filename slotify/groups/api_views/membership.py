from rest_framework.decorators import api_view
from rest_framework.response import Response
from groups.methods import is_group_admin
from groups.permissions import GroupAdminPermission
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from groups.serializers import (
    UserSerializer,
    MembershipSerializer,
    MembershipRequestSerializer,
    MembershipUpdateSerializer,
)
from groups.models import Membership, Group
from authentication.models import User
from rest_framework.permissions import (
    BasePermission,
    IsAuthenticated,
)

@api_view(['POST'])
def check_is_group_admin(request):
    """
    Checks if the user is a group admin
    """
    print(request.data)
    if is_group_admin(request.user, request.data["group"]):
        return Response({'is_group_admin': True})
    else:
        return Response({'is_group_admin': False})

class MembersList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_fields = ("group",)


class GroupListPermission(BasePermission):
    def has_permission(self, request, view):
        group = Group.objects.get(id=view.kwargs["id"])
        return is_group_admin(request.user, group)


class MembershipList(ListAPIView):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
    permission_classes = [IsAuthenticated & GroupListPermission]
    filter_fields = ("user",)
    def get_queryset(self):
        queryset = super().get_queryset()
        group_id = self.kwargs["id"]
        if group_id is not None:
            queryset = queryset.filter(group=group_id).order_by("group")
        return queryset


class MembershipRequest(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MembershipRequestSerializer

    def create(self, request, *args, **kwargs):
        request.data["user"] = request.user.pk
        return super().create(request, *args, **kwargs)


class MembershipRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    lookup_field = "id"
    queryset = Membership.objects.all()
    serializer_class = MembershipUpdateSerializer
    permission_classes = [IsAuthenticated & GroupAdminPermission]
