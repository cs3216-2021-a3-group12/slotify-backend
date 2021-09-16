from .models import Event, Slot, SignUp
from common.constants import TITLE, DESCRIPTION, START_DATE_TIME, END_DATE_TIME, LOCATION, IS_PUBLIC
from common.parsers import parse_datetime_to_epoch_time

def get_events(*args, **kwargs):
    return Event.objects.filter(*args, **kwargs)

def get_slots(*args, **kwargs):
    return Slot.objects.filter(*args, **kwargs)

def get_signups(*args, **kwargs):
    return SignUp.objects.filter(*args, **kwargs)

def event_to_json(event):
    data = {
        TITLE: event.title,
        DESCRIPTION: event.description,
        START_DATE_TIME: parse_datetime_to_epoch_time(event.start_date_time),
        END_DATE_TIME: parse_datetime_to_epoch_time(event.end_date_time),
        LOCATION: event.location,
        IS_PUBLIC: event.is_public,
        # TODO: include group to json here
    }

    # TODO: include info about slots if necessary (eg. how many signed up, how many slots left etc)
    
    return data

def get_slot_availability_data(slot):
    # Get number of remaining slots
    confirmed_signups = len(get_signups(slot=slot, is_confirmed=True))
    pending_signups = len(get_signups(slot=slot, is_confirmed=False))
    available_slots = slot.limit - confirmed_signups

    data = {
        "tag_name": slot.tag.name,
        "tag_id": slot.tag.id,
        "confirmed": confirmed_signups,
        "pending": pending_signups,
        "available_slots": available_slots
    }

    return data
