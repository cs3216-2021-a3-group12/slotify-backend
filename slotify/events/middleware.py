from rest_framework.exceptions import NotFound

from .models import Event, Slot, SignUp
from .methods import get_events, get_slots, get_signups

def check_event_exists(view_method):
    def _arguments_wrapper(instance, request, event_id, *args, **kwargs):
        try:
            event = (
                get_events(id=event_id)
                .select_related("group")
                .get()
            )
        except Event.DoesNotExist:
            raise NotFound(
                detail="No event found.",
                code="no_event_found",
            )

        return view_method(instance, request, event=event, *args, **kwargs)

    return _arguments_wrapper


def check_slot_exists(view_method):
    def _arguments_wrapper(instance, request, slot_id, *args, **kwargs):
        try:
            slot = (
                get_slots(id=slot_id)
                .select_related("tag", "event")
                .get()
            )
        except Slot.DoesNotExist:
            raise NotFound(
                detail="No slot found.",
                code="no_slot_found",
            )

        return view_method(instance, request, slot=slot, *args, **kwargs)

    return _arguments_wrapper


def check_signup_exists(view_method):
    def _arguments_wrapper(instance, request, signup_id, *args, **kwargs):
        try:
            signup = (
                get_signups(id=signup_id)
                .select_related("user", "slot")
                .get()
            )
        except SignUp.DoesNotExist:
            raise NotFound(
                detail="No signup found.",
                code="no_signup_found",
            )

        return view_method(instance, request, signup=signup, *args, **kwargs)

    return _arguments_wrapper