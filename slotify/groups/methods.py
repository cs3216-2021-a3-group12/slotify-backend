from .models import Group, Membership
from common.constants import (
    GROUP_NAME, GROUP_ID, GROUP_DESCRIPTION, DATE_CREATED, BANNER_URL, CATEGORY,
    CATEGORY_ID, CATEGORY_NAME
)
from common.parsers import parse_datetime_to_epoch_time


def get_groups(*args, **kwargs):
    return Group.objects.filter(*args, **kwargs)


def get_memberships(*args, **kwargs):
    return Membership.objects.filter(*args, **kwargs)


def get_user_group_membership(user, group):
    try:
        return get_memberships(user=user, group=group).get()
    except Membership.DoesNotExist:
        return None

def group_to_json(group, include_more_details=True):
    data = {
        GROUP_ID: group.id,
        GROUP_NAME: group.name,
        BANNER_URL: group.banner_url,
        CATEGORY: {
            CATEGORY_ID: group.category.id,
            CATEGORY_NAME: group.category.name
        }
    }

    if include_more_details:
        data[GROUP_DESCRIPTION] = group.description
        data[DATE_CREATED] = parse_datetime_to_epoch_time(group.date_created)
    
    return data
    
def is_group_admin(user, group):
    membership = get_user_group_membership(user, group)
    if membership:
        return membership.is_approved & membership.is_admin
    return False
