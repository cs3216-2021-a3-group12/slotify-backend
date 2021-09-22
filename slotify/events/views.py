from groups.methods import is_group_admin
from groups.permissions import EventGroupAdminPermission
from authentication.middleware import check_requester_is_authenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from .models import Event, Slot, Tag
from .methods import event_to_json
from authentication.middleware import check_requester_is_authenticated
from groups.middleware import check_group_exists, check_requester_is_group_admin
from common.parsers import parse_epoch_timestamp_to_datetime
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
)
from .serializers import PostEventSerializer, EventSerializer, EventUpdateSerializer
from events.methods import get_signups, signup_to_json, event_to_json
from common.constants import EVENT, SIGNUP
import json


class GroupEventsView(APIView):
    parser_classes = [FormParser, MultiPartParser]

    @check_requester_is_authenticated
    @check_group_exists
    @check_requester_is_group_admin
    def post(self, request, requester, group):

        serializer = PostEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        slots = json.loads(request.data.get("slots"))

        # Create but don't save event first
        start_date_time = validated_data.get("start_date_time")
        end_date_time = validated_data.get("end_date_time")

        new_event = Event(
            title=validated_data.get("title", ""),
            description=validated_data.get("description", ""),
            group=group,
            start_date_time=parse_epoch_timestamp_to_datetime(start_date_time),
            end_date_time=parse_epoch_timestamp_to_datetime(end_date_time),
            location=validated_data.get("location", ""),
            is_public=validated_data.get("is_public"),
            image_url=validated_data.get("image_url", ""),
        )

        new_event.save()
        for tag_name, limit in slots.items():
            # TODO: might need to handle case where tag name is invalid (doesn't exist)
            # Alternatively, we can assume this case will not happen if frontend strictly
            # uses tag names fetched
            new_slot = Slot(
                event=new_event, limit=limit, tag=Tag.objects.get(name=tag_name)
            )
            new_slot.save()

        return Response(event_to_json(new_event), status=status.HTTP_201_CREATED)


class UserSignedUpEventsView(APIView):
    @check_requester_is_authenticated
    def get(self, request, requester):
        all_events_data = []

        all_signups = get_signups(user=requester).order_by("-created_at")
        for signup in all_signups:
            event = signup.slot.event
            event_data = {
                EVENT: event_to_json(event),
                SIGNUP: signup_to_json(signup, include_user=False),
            }
            all_events_data.append(event_data)

        return Response(all_events_data, status=status.HTTP_200_OK)


class EventListView(ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_fields = ("id", "group", "is_public")
    search_fields = ("title", "description")


class EventRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    lookup_field = "id"
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly & EventGroupAdminPermission]

    def get_serializer_class(self):
        if self.request.method in ["PATCH", "POST"]:
            return EventUpdateSerializer
        return super().get_serializer_class()

    def update(self, request, *args, **kwargs):
        if request.data.get("start_date_time") is not None:
            request.data["start_date_time"] = parse_epoch_timestamp_to_datetime(
                request.data.get("start_date_time")
            )
        if request.data.get("end_date_time") is not None:
            request.data["end_date_time"] = parse_epoch_timestamp_to_datetime(
                request.data.get("end_date_time")
            )
        return super().update(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # check if user is group admin
        is_admin = is_group_admin(request.user, instance.group)
        instance.is_admin = is_admin
        serializer = self.get_serializer(instance)
        return Response(serializer.data)