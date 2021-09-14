from django.db.models.query import QuerySet
from .models import Group

def get_groups(*args, **kwargs) -> QuerySet[Group]:
    return Group.objects.filter(*args, **kwargs)
