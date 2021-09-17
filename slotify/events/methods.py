from .models import Event, Slot, SignUp
from common.constants import (
    TITLE, DESCRIPTION, START_DATE_TIME, END_DATE_TIME, LOCATION, IS_PUBLIC, EVENT, SLOT, TAG_NAME,
    TAG_ID, CONFIRMED_SIGNUP_COUNT, PENDING_SIGNUP_COUNT, AVAILABLE_SLOT_COUNT, SIGNUP_DATE, IS_CONFIRMED)
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

def signup_to_json(signup):
    data = {
        SLOT: slot_to_json(signup.slot),
        SIGNUP_DATE: parse_datetime_to_epoch_time(signup.created_at),
        IS_CONFIRMED: signup.is_confirmed
    }

    return data

def get_slot_availability_data(slot):
    confirmed_signups = len(get_signups(slot=slot, is_confirmed=True))
    pending_signups = len(get_signups(slot=slot, is_confirmed=False))
    available_slots = slot.limit - confirmed_signups

    return confirmed_signups, pending_signups, available_slots

def slot_to_json(slot, include_availability=False):
    data = {
        TAG_NAME: slot.tag.name,
        TAG_ID: slot.tag.id,
    }

    if include_availability:
        confirmed, pending, available = get_slot_availability_data(slot)

        data[CONFIRMED_SIGNUP_COUNT] = confirmed
        data[PENDING_SIGNUP_COUNT] = pending
        data[AVAILABLE_SLOT_COUNT] = available

    return data

def is_general_group_slot(slot):
    return slot.tag.name == "GroupMember"