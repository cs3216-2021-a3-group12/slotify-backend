from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from groups.serializers import GroupSerializer, GroupCreateSerializer
from groups.models import Group, Membership
from authentication.models import User
from rest_framework.permissions import (
    IsAuthenticated,
    BasePermission,
)
from groups.methods import get_memberships


class GroupsPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100


class GroupList(ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = GroupsPagination
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ("category",)
    search_fields = ("name", "description")


class GroupCreate(CreateAPIView):
    serializer_class = GroupCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        group = serializer.save()
        group.members.add(
            self.request.user, through_defaults={"is_admin": True, "is_approved": True}
        )


class GroupAdminPermission(BasePermission):
    def has_permission(self, request, view):
        group = view.get_object()
        try:
            membership = get_memberships(group=group, user=request.user).get()
            return membership.is_approved and membership.is_admin
        except (Membership.DoesNotExist):
            return False


class GroupRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    lookup_field = "id"
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated & GroupAdminPermission]
