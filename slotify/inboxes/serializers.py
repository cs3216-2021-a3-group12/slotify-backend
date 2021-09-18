from .models import Message
from rest_framework import serializers

class MessageSerializer(serializers.ModelSerializer):
    created_at = serializers.ReadOnlyField()
    id = serializers.ReadOnlyField()
    class Meta:
        model = Message
        fields = ('id', 'title', 'content', 'read', 'created_at')

class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('title', 'content', 'receiver')
