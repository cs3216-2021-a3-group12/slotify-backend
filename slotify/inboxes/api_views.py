from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import MessageSerializer, MessageCreateSerializer
from .models import Message



class MessageCreateView(CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageCreateSerializer
    
class MessageListView(ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(receiver=self.request.user)

class MessageUpdateView(UpdateAPIView):
    lookup_field = 'id'
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(receiver=self.request.user)