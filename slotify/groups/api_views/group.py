from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from groups.serializers import GroupSerializer, GroupCreateSerializer
from groups.models import Group
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from groups.permissions import GroupAdminPermission


class GroupList(ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_fields = ("category",)
    search_fields = ("name", "description")


class GroupCreate(CreateAPIView):
    serializer_class = GroupCreateSerializer
    # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        group = serializer.save()
        group.members.add(
            self.request.user, through_defaults={"is_admin": True, "is_approved": True}
        )


class GroupRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    lookup_field = "id"
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticatedOrReadOnly & GroupAdminPermission]
