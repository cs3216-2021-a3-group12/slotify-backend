from groups.permissions import GroupAdminPermission
from authentication.middleware import check_requester_is_authenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView

from authentication.models import User
from groups.models import Group
from .models import Event, Slot, Tag
from .methods import event_to_json
from authentication.middleware import check_requester_is_authenticated
from groups.middleware import check_group_exists, check_requester_is_group_admin
from common.parsers import parse_epoch_timestamp_to_datetime
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
)
from .serializers import PostEventSerializer, EventSerializer


class GroupEventsView(APIView):
    @check_requester_is_authenticated
    @check_group_exists
    @check_requester_is_group_admin
    def post(self, request, requester: User, group: Group):
        serializer = PostEventSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

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
        )

        new_event.save()

        slots = validated_data.get("slots")
        for tag_name, limit in slots.items():
            # TODO: might need to handle case where tag name is invalid (doesn't exist)
            # Alternatively, we can assume this case will not happen if frontend strictly
            # uses tag names fetched
            new_slot = Slot(
                event=new_event, limit=limit, tag=Tag.objects.get(name=tag_name)
            )
            new_slot.save()

        return Response(event_to_json(new_event), status=status.HTTP_201_CREATED)


class EventListView(ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_fields = ("id", "group", "is_public")
    search_fields = ("title", "description")


class EventRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    lookup_field = "id"
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly & GroupAdminPermission]
