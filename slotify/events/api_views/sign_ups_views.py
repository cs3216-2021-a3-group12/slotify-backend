from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from authentication.middleware import check_requester_is_authenticated
from events.methods import get_slots
from events.middleware import check_event_exists, check_slot_exists
from events.methods import get_slot_availability_data, slot_to_json, get_signups, signup_to_json, is_general_group_slot
from events.models import Slot, Event, SignUp
from groups.models import Group, Tag, Membership
from groups.methods import get_memberships

from common.constants import MESSAGE, SIGN_UP

class SlotsView(APIView):
    @check_event_exists
    def get(self, request, event):
        slots = get_slots(event=event)

        formatted_slots = []

        for slot in slots:
            slot_data = slot_to_json(slot, include_availability=True)
            formatted_slots.append(slot_data)

        return Response(data=formatted_slots, status=status.HTTP_200_OK)

class SingleSlotView(APIView):
    @check_slot_exists
    def get(self, request, slot):
        return Response(
            data=slot_to_json(slot, include_availability=True), status=status.HTTP_200_OK
        )

    # TODO: endpoints for updating slot
    @check_slot_exists
    def put(self, request, slot):
        # check if increase/decrease against membership
        pass


class PostSignUpView(APIView):
    @check_requester_is_authenticated
    @check_slot_exists
    def post(self, request, requester, slot):
        event = slot.event
        group = event.group
        slot_tag = slot.tag

         # Check if user already signed up for another slot
        try:
            existing_signup = get_signups(slot__event=event, user=requester).get()
            if existing_signup and existing_signup.is_confirmed:
                data = {
                    MESSAGE: "Already signed up for this event",
                    SIGN_UP: signup_to_json(existing_signup)
                }

                return Response(data, status.HTTP_400_BAD_REQUEST)
        except SignUp.DoesNotExist:
            pass

        # If this slot is exclusive to group members only, ensure requester is group member
        if slot_tag.is_exclusive_to_groups:
            try:
                membership = get_memberships(user=requester, group=group).get()
                if not membership.is_approved:
                    raise Membership.DoesNotExist
            except Membership.DoesNotExist:
                raise PermissionDenied(detail="Not group member", code="not_group_member")
                
            # Check if this is a general slot (any group members can join this slot regardless of tag)
            # If not general slot, check if member has a matching slot tag
            if not is_general_group_slot(slot) and slot_tag != membership.tag:
                raise PermissionDenied(detail="Not eligible to signup for slot", code="not_eligible_slot")

        _, pending, available = get_slot_availability_data(slot)
        current_signup_can_be_confirmed = pending == 0 and available > 0

        new_signup = SignUp(
            slot=slot,
            user=requester,
            is_confirmed=current_signup_can_be_confirmed
        )
        new_signup.save()

        data = {
            MESSAGE: "Successfully signed up",
            SIGN_UP: signup_to_json(new_signup)
        }
        
        return Response({MESSAGE: "Signed up", }, status.HTTP_201_CREATED)