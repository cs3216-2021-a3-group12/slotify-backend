from django.db.utils import IntegrityError
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from authentication.middleware import check_requester_is_authenticated, check_requester_has_profile
from events.methods import get_slots
from events.middleware import check_event_exists, check_slot_exists, check_signup_exists
from events.methods import (
    slot_to_json, get_slot_availability_data, is_general_group_slot,
    signup_to_json, get_existing_signup_for_any_event_slot, get_signups, get_existing_signup_for_slot
)
from events.models import SignUp
from groups.methods import get_user_group_membership
from events.serializers import UpdateSignUpSerializer

from common.constants import MESSAGE, SIGNUP, HAS_ATTENDED

class SlotsView(APIView):
    @check_requester_is_authenticated
    @check_event_exists
    def get(self, request, requester, event):
        slots = get_slots(event=event)

        formatted_slots = []

        for slot in slots:
            slot_data = slot_to_json(slot, user=requester)
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


class PostDeleteSignUpView(APIView):
    @check_requester_is_authenticated
    @check_requester_has_profile
    @check_slot_exists
    def post(self, request, requester, slot):
        event = slot.event
        group = event.group
        slot_tag = slot.tag

        # Check if user already signed up for another slot
        existing_signup = get_existing_signup_for_any_event_slot(event=slot.event, user=requester)
        if existing_signup:
            data = {
                MESSAGE: "Already signed up for this event",
                SIGNUP: signup_to_json(existing_signup, include_user=False)
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
                SIGNUP: signup_to_json(new_signup, include_user=False)
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(
                {MESSAGE: "An error occurred, please try again later"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        data = {
            MESSAGE: "Successfully signed up",
            SIGNUP: signup_to_json(new_signup, include_user=False)
        }
        
        return Response(data, status=status.HTTP_201_CREATED)

    @check_requester_is_authenticated
    @check_slot_exists
    def delete(self, request, requester, slot):
        existing_signup = get_existing_signup_for_slot(slot=slot, user=requester)

        if not existing_signup:
            data = {
                MESSAGE: "No signup found",
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        existing_signup.delete()

        slot = existing_signup.slot

        _, _, available = get_slot_availability_data(slot)
        pending_signups = get_signups(slot=slot, is_confirmed=False).order_by("created_at")

        for pending_signup in pending_signups:
            if not available:
                break

            pending_signup.is_confirmed = True
            pending_signup.save()
            available -= 1

            # TODO: send email/phone notification to previously waitlisted members

        data = {
            MESSAGE: "Sign up for this slot withdrawn."
        }
        return Response(data, status=status.HTTP_200_OK)


class AdminGetSignUpsView(APIView):
    @check_requester_is_authenticated
    @check_event_exists
    def get(self, request, requester, event):
        # check if requester is admin of the group which is hosting event
        membership = get_user_group_membership(user=requester, group=event.group)
        if not membership or not membership.is_approved or not membership.is_admin:
            raise PermissionDenied(
                detail="Not group admin, no permission to view all signups",
                code="not_group_admin"
            )

        event_slots = get_slots(event=event)

        data = [
            slot_to_json(
                slot=slot, include_availability=True, include_signups=True
            ) for slot in event_slots
        ]

        return Response(data, status=status.HTTP_200_OK)


class AdminUpdateSignUpsView(APIView):
    @check_requester_is_authenticated
    @check_signup_exists
    def put(self, request, requester, signup):
        group = signup.slot.event.group
        # check if requester is admin of the group which is hosting event
        membership = get_user_group_membership(user=requester, group=group)
        if not membership or not membership.is_approved or not membership.is_admin:
            raise PermissionDenied(
                detail="Not group admin, no permission to view all signups",
                code="not_group_admin"
            )

        serializer = UpdateSignUpSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        has_attended = validated_data.get(HAS_ATTENDED)

        signup.has_attended = has_attended
        signup.save()

        # updated signup
        return Response(signup_to_json(signup), status=status.HTTP_200_OK)