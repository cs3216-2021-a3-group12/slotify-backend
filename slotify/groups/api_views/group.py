from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView

from groups.serializers import GroupSerializer
from groups.models import Group

class GroupList(ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class GroupCreate(CreateAPIView):
    serializer_class = GroupSerializer

class GroupRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = Group.objects.all()
    serializer_class = GroupSerializer