from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from authentication.middleware import check_requester_is_authenticated
from events.methods import get_slots
from events.middleware import check_event_exists, check_slot_exists
from events.methods import get_slot_availability_data
from events.models import Slot
from groups.models import Group, Tag

class SlotsView(APIView):
    @check_event_exists
    def get(self, request, event):
        slots = get_slots(event=event)

        parsed_slots = []

        for slot in slots:
            slot_data = get_slot_availability_data(slot)
            parsed_slots.append(slot_data)

        return Response(data=parsed_slots, status=status.HTTP_200_OK)

class SingleSlotView(APIView):
    @check_slot_exists
    def get(self, request, slot):
        return Response(data=get_slot_availability_data(slot), status=status.HTTP_200_OK)


class PostSignUpView(APIView):
    @check_requester_is_authenticated
    @check_slot_exists
    def post(self, request, requester, slot):
        # TODO: check that no other signup for other slots for the same event exists

        # anyone can sign up, even if they are not from the group
        if not slot.tag.is_exclusive_to_groups:
            pass
            


        # only members can sign up
        # membership = (
        #     get_memberships(group=group, user=requester)
        #     .get()
        # )