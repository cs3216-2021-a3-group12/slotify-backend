from .models import Group, Membership


def get_groups(*args, **kwargs):
    return Group.objects.filter(*args, **kwargs)


def get_memberships(*args, **kwargs):
    return Membership.objects.filter(*args, **kwargs)


def get_user_group_membership(user, group):
    try:
        return get_memberships(user=user, group=group).get()
    except Membership.DoesNotExist:
        return None