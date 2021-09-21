from .models import Event, Slot, SignUp
from groups.methods import get_user_group_membership, group_to_json
from authentication.methods import user_to_json
from common.parsers import parse_datetime_to_epoch_time

# Constants
from common.constants import (
    EVENT_ID,
    TITLE,
    DESCRIPTION,
    START_DATE_TIME,
    END_DATE_TIME,
    LOCATION,
    IS_PUBLIC,
    GROUP,
    IMAGE_URL,
)
from common.constants import TAG, TAG_NAME, TAG_ID
from common.constants import (
    SLOT,
    SLOT_ID,
    SIGNUP_ID,
    CONFIRMED_SIGNUP_COUNT,
    PENDING_SIGNUP_COUNT,
    AVAILABLE_SLOT_COUNT,
    SIGNUP_DATE,
    IS_CONFIRMED,
    IS_ELIGIBLE,
    IS_SIGNED_UP,
    GENERAL_GROUP_TAG_NAME,
    SIGNUPS,
    CONFIRMED_SIGNUPS,
    PENDING_SIGNUPS,
    USER,
    HAS_ATTENDED
)


def get_events(*args, **kwargs):
    return Event.objects.filter(*args, **kwargs)


def get_slots(*args, **kwargs):
    return Slot.objects.filter(*args, **kwargs)


def get_signups(*args, **kwargs):
    return SignUp.objects.filter(*args, **kwargs)


def event_to_json(event, include_group=True):
    data = {
        EVENT_ID: event.id,
        TITLE: event.title,
        DESCRIPTION: event.description,
        START_DATE_TIME: parse_datetime_to_epoch_time(event.start_date_time),
        END_DATE_TIME: parse_datetime_to_epoch_time(event.end_date_time),
        LOCATION: event.location,
        IS_PUBLIC: event.is_public,
    }
    if event.image_url:
        data[IMAGE_URL] = event.image_url.url
    if include_group:
        data[GROUP] = group_to_json(event.group)
    return data


def signup_to_json(signup, include_slot=True, include_user=True):
    data = {
        SIGNUP_ID: signup.id,
        SIGNUP_DATE: parse_datetime_to_epoch_time(signup.created_at),
        IS_CONFIRMED: signup.is_confirmed,
        HAS_ATTENDED: signup.has_attended,
    }

    if include_slot:
        data[SLOT] = slot_to_json(signup.slot, include_availability=False)

    if include_user:
        data[USER] = user_to_json(signup.user)

    return data


def get_slot_availability_data(slot):
    confirmed_signups = len(get_signups(slot=slot, is_confirmed=True))
    pending_signups = len(get_signups(slot=slot, is_confirmed=False))
    available_slots = slot.limit - confirmed_signups

    return confirmed_signups, pending_signups, available_slots


def get_existing_signup_for_slot(slot, user):
    try:
        return get_signups(slot=slot, user=user).get()
    except SignUp.DoesNotExist:
        return None


def get_existing_signup_for_any_event_slot(event, user):
    try:
        return get_signups(slot__event=event, user=user).get()
    except SignUp.DoesNotExist:
        return None


def slot_to_json(slot, include_availability=True, user=None, include_signups=False):
    data = {TAG: {TAG_NAME: slot.tag.name, TAG_ID: slot.tag.id}, SLOT_ID: slot.id}

    if include_availability:
        confirmed, pending, available = get_slot_availability_data(slot)

        data[CONFIRMED_SIGNUP_COUNT] = confirmed
        data[PENDING_SIGNUP_COUNT] = pending
        data[AVAILABLE_SLOT_COUNT] = available

    if include_signups:
        confirmed_signups = get_signups(slot=slot, is_confirmed=True)
        pending_signups = get_signups(slot=slot, is_confirmed=False)

        signup_data = {
            CONFIRMED_SIGNUPS: [
                signup_to_json(signup, include_slot=False)
                for signup in confirmed_signups
            ],
            PENDING_SIGNUPS: [
                signup_to_json(signup, include_slot=False) for signup in pending_signups
            ],
        }

        data[SIGNUPS] = signup_data

    # If user is specified, return user-specific data for the slot
    if not user:
        return data

    existing_signup = get_existing_signup_for_slot(slot, user)
    data[IS_SIGNED_UP] = existing_signup is not None
    data[IS_CONFIRMED] = existing_signup is not None and existing_signup.is_confirmed

    is_eligible = True

    if slot.tag.is_exclusive_to_groups:
        group = slot.event.group
        membership = get_user_group_membership(user=user, group=group)
        if membership is None or not membership.is_approved:
            is_eligible = False

        # Check if this is a general slot (any group members can join this slot regardless of tag)
        # If not general slot, check if member has a matching slot tag
        if (
            not is_general_group_slot(slot)
            and membership
            and slot.tag != membership.tag
        ):
            is_eligible = False

    data[IS_ELIGIBLE] = is_eligible

    return data


def is_general_group_slot(slot):
    return slot.tag.name == GENERAL_GROUP_TAG_NAME
