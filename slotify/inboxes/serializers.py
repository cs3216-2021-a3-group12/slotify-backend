from .models import Message
from rest_framework import serializers

class MessageSerializer(serializers.ModelSerializer):
    created_at = serializers.ReadOnlyField()
    class Meta:
        model = Message
        fields = ('id', 'text', 'user', 'is_read', 'created_at')
