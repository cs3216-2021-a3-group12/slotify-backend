from .models import User
from django.db.models import QuerySet

from common.constants import USERNAME, EMAIL

def get_users(*args, **kwargs):
    return User.objects.filter(*args, **kwargs)


def user_to_json(user):
    data = {
        USERNAME: user.username,
        EMAIL: user.email
    }
    return data