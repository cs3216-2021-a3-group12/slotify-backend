from .models import Message
from rest_framework import serializers

class MessageSerializer(serializers.ModelSerializer):
    created_at = serializers.ReadOnlyField()
    class Meta:
        model = Message
        fields = ('id', 'title', 'content', 'read', 'created_at')
