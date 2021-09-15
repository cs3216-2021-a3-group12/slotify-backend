from groups.methods import get_memberships
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend

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


class MembershipPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100


class MembersList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = MembershipPagination
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("group",)


class GroupListPermission(BasePermission):
    def has_permission(self, request, view):
        group = Group.objects.get(id=view.kwargs["id"])

        try:
            membership = get_memberships(group=group, user=request.user).get()
            print(membership)
            return membership.is_approved and membership.is_admin
        except (Membership.DoesNotExist):
            return False


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


class GroupAdminPermission(BasePermission):
    def has_permission(self, request, view):
        group = view.get_object().group
        try:
            membership = get_memberships(group=group, user=request.user).get()
            print(membership)
            return membership.is_approved and membership.is_admin
        except (Membership.DoesNotExist):
            return False


class MembershipRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    lookup_field = "id"
    queryset = Membership.objects.all()
    serializer_class = MembershipUpdateSerializer
    permission_classes = [IsAuthenticated & GroupAdminPermission]
