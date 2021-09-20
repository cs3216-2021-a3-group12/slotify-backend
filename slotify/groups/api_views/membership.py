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
