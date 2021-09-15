from .models import Group, Membership


def get_groups(*args, **kwargs):
    return Group.objects.filter(*args, **kwargs)


def get_memberships(*args, **kwargs):
    return Membership.objects.filter(*args, **kwargs)
