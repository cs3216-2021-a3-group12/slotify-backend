from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView

from groups.serializers import TagSerializer
from groups.models import Tag

class TagList(ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class TagCreate(CreateAPIView):
    serializer_class = TagSerializer

class TagRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = Tag.objects.all()
    serializer_class = TagSerializer