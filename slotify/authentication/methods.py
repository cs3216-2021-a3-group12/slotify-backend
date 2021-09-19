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

def nusnet_id_exists(nusnet_id):
    try:
        existing_user = get_users(nusnet_id=nusnet_id).get()
        if existing_user:
            return True
    except User.DoesNotExist:
        return False

def student_number_exists(student_number):
    try:
        existing_user = get_users(student_number=student_number).get()
        if existing_user:
            return True
    except User.DoesNotExist:
        return False
