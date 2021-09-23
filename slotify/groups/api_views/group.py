from groups.methods import is_group_admin
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.response import Response
from groups.serializers import GroupSerializer, GroupCreateSerializer
from groups.models import Group, Membership, Category
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


class MyGroupList(ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_fields = ("category",)
    search_fields = ("name", "description")

    def get_queryset(self):
        """
        This view should return a list of all the groups
        for the currently authenticated user.
        """
        user = self.request.user
        group_ids = Membership.objects.filter(user=user, is_approved=True).values_list(
            "group_id", flat=True
        )
        return Group.objects.filter(id__in=group_ids)


class GroupCreate(CreateAPIView):
    serializer_class = GroupCreateSerializer
    permission_classes = [IsAuthenticated]

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

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        record = Membership.objects.filter(
                user=request.user, group=instance).first()
        instance.is_approved = record.is_approved
        instance.is_admin = record.is_admin
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        if request.data.get("category") is not None:
            instance = self.get_object()
            category_id = request.data.get("category")
            category = Category.objects.get(id=category_id)
            instance.category = category
        partial = kwargs.pop("partial", False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
