from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView

from groups.serializers import CategorySerializer
from groups.models import Category

class CategoryList(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryCreate(CreateAPIView):
    serializer_class = CategorySerializer

class CategoryRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer