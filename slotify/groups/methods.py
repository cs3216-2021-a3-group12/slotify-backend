from django.db.models.query import QuerySet
from .models import Group, Membership

def get_groups(*args, **kwargs) -> QuerySet[Group]:
    return Group.objects.filter(*args, **kwargs)

def get_memberships(*args, **kwargs) -> QuerySet[Membership]:
    return Membership.objects.filter(*args, **kwargs)