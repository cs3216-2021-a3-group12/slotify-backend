from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from groups.serializers import GroupSerializer, GroupCreateSerializer
from groups.models import Group

class GroupsPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100
class GroupList(ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = GroupsPagination
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('category',)
    search_fields = ('name', 'description')

class GroupCreate(CreateAPIView):
    serializer_class = GroupCreateSerializer

    def perform_create(self, serializer):
        group = serializer.save()
        # add creator to group via memberhip creation
        group.members.add(self.request.user)

class GroupRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = Group.objects.all()
    serializer_class = GroupSerializer