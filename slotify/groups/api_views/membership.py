from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend

from groups.serializers import UserSerializer, MembershipSerializer
from groups.models import Membership
from authentication.models import User


class MembershipPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100


class MembersList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = MembershipPagination
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("group",)

    # override filter queryset
    def get_queryset(self):
        queryset = super().get_queryset()
        group_id = self.request.query_params.get("group", None)
        if group_id is not None:
            queryset = queryset.filter(group=group_id).order_by("group")
        return queryset


class MembershipList(ListAPIView):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer


class MembershipCreate(CreateAPIView):
    serializer_class = MembershipSerializer


class MembershipRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    lookup_field = "id"
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
