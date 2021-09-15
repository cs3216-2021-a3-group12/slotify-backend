from .models import User
from django.db.models import QuerySet

def get_users(*args, **kwargs) -> QuerySet[User]:
    return User.objects.filter(*args, **kwargs)