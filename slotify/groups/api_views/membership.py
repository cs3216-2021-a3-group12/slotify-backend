from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView

from groups.serializers import MembershipSerializer
from groups.models import Membership

class MembershipList(ListAPIView):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer

class MembershipCreate(CreateAPIView):
    serializer_class = MembershipSerializer

class MembershipRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer