from rest_framework.exceptions import NotFound

from .models import Event, Slot
from .methods import get_events, get_slots

def check_event_exists(view_method):
    def _arguments_wrapper(instance, request, event_id, *args, **kwargs):
        try:
            event = get_events(id=event_id).get()
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