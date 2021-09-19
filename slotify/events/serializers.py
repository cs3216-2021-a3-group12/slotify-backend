from common.parsers import (
    parse_datetime_to_epoch_time,
)
from rest_framework import serializers

from .models import Event, Slot, SignUp
from common.constants import (
    EVENT_MAX_TITLE_LENGTH,
    EVENT_MIN_TITLE_LENGTH,
    EVENT_MAX_LOCATION_LENGTH,
)


class PostEventSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        max_length=EVENT_MAX_TITLE_LENGTH, min_length=EVENT_MIN_TITLE_LENGTH
    )
    description = serializers.CharField()
    start_date_time = serializers.IntegerField(min_value=0)
    end_date_time = serializers.IntegerField(min_value=0)
    location = serializers.CharField(max_length=EVENT_MAX_LOCATION_LENGTH)
    is_public = serializers.BooleanField()
    slots = serializers.DictField(child=serializers.IntegerField(min_value=1))
    image_url = serializers.ImageField(required=False, default=None)

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
        fields = [
            "title",
            "description",
            "start_date_time",
            "end_date_time",
            "location",
            "is_public",
            "slots",
            "image_url",
        ]


class SlotSerializer(serializers.ModelSerializer):
    """
    Serializer for the event slots.
    """

    class Meta:
        model = Slot
        fields = ["user", "event"]


class EventSerializer(serializers.ModelSerializer):
    start_date_time = serializers.SerializerMethodField()
    end_date_time = serializers.SerializerMethodField()

    def get_start_date_time(self, obj):
        return parse_datetime_to_epoch_time(obj.start_date_time)

    def get_end_date_time(self, obj):
        return parse_datetime_to_epoch_time(obj.end_date_time)

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "start_date_time",
            "end_date_time",
            "location",
            "is_public",
            "group",
            "image_url",
        ]


class EventUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "start_date_time",
            "end_date_time",
            "location",
            "is_public",
            "image_url",
        ]


class UpdateSignUpSerializer(serializers.ModelSerializer):
    has_attended = serializers.BooleanField()

    class Meta:
        model = SignUp
        fields = ["has_attended"]
