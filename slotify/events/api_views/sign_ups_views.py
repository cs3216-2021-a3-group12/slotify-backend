from django.db.utils import IntegrityError
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from authentication.middleware import check_requester_is_authenticated
from events.methods import get_slots
from events.middleware import check_event_exists, check_slot_exists
from events.methods import (
    slot_to_json, get_slot_availability_data, is_general_group_slot,
    signup_to_json, get_existing_signup,
)
from events.models import SignUp
from groups.models import Membership
from groups.methods import get_user_group_membership

from common.constants import MESSAGE, SIGNUP

class SlotsView(APIView):
    @check_event_exists
    def get(self, request, event):
        slots = get_slots(event=event)

        formatted_slots = []

        for slot in slots:
            slot_data = slot_to_json(slot)
            formatted_slots.append(slot_data)

        return Response(data=formatted_slots, status=status.HTTP_200_OK)

class SingleSlotView(APIView):
    @check_requester_is_authenticated
    @check_slot_exists
    def get(self, request, requester, slot):
        return Response(
            data=slot_to_json(slot, user=requester), status=status.HTTP_200_OK
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
        existing_signup = get_existing_signup(slot=slot, user=requester)
        if existing_signup:
            data = {
                    MESSAGE: "Already signed up for this event",
                    SIGNUP: signup_to_json(existing_signup)
                }

            return Response(data, status=status.HTTP_400_BAD_REQUEST)


        # If this slot is exclusive to group members only, ensure requester is group member
        if slot_tag.is_exclusive_to_groups:
            membership = get_user_group_membership(user=requester, group=group)
            if membership is None or not membership.is_approved:
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
        try:
            new_signup.save()
        except IntegrityError:
            data = {
                MESSAGE: "Already signed up for this event",
                SIGNUP: signup_to_json(new_signup)
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(
                {MESSAGE: "An error occurred, please try again later"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        data = {
            MESSAGE: "Successfully signed up",
            SIGNUP: signup_to_json(new_signup)
        }
        
        return Response(data, status=status.HTTP_201_CREATED)