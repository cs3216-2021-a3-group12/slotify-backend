from .models import Event
from common.constants import TITLE, DESCRIPTION, START_DATE_TIME, END_DATE_TIME, LOCATION, IS_PUBLIC
from common.parsers import parse_datetime_to_epoch_time

# TODO: extract event creation here for better abstraction
def create_event() -> Event:
    pass

def event_to_json(event: Event):
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