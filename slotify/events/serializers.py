from rest_framework import serializers

from .models import Event
from common.constants import (
    EVENT_MAX_TITLE_LENGTH,
    EVENT_MIN_TITLE_LENGTH,
    EVENT_MAX_LOCATION_LENGTH
)

class PostEventSerializer(serializers.ModelSerializer):
    title=serializers.CharField(max_length=EVENT_MAX_TITLE_LENGTH, min_length=EVENT_MIN_TITLE_LENGTH)
    description=serializers.CharField()
    start_date_time = serializers.IntegerField(min_value=0)
    end_date_time = serializers.IntegerField(min_value=0)
    location = serializers.CharField(max_length=EVENT_MAX_LOCATION_LENGTH)
    is_public = serializers.BooleanField()

    def validate(self, data):
        """
        Check that start_date_time is before end_date_time.
        """
        if data["start_date_time"] >= data["end_date_time"]:
            raise serializers.ValidationError(
                "start date/time must be before end date/time"
            )
        return data

    
    class Meta:
        model = Event
        fields = ["title", "description", "start_date_time", "end_date_time", "location", "is_public"]

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["id", "title", "description", "start_date_time", "end_date_time", "location", "is_public"]