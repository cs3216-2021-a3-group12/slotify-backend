from datetime import datetime
from django.utils.timezone import make_aware

def parse_epoch_timestamp_to_datetime(epoch_timestamp: int) -> datetime:
    return make_aware(datetime.fromtimestamp(epoch_timestamp))

def parse_datetime_to_epoch_time(date: datetime) -> int:
    return round(date.timestamp())