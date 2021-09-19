from .models import User
from django.db.models import QuerySet

from common.constants import USERNAME, EMAIL, TELEGRAM_HANDLE, STUDENT_NUMBER, NUSNET_ID

def get_users(*args, **kwargs):
    return User.objects.filter(*args, **kwargs)


def user_to_json(user):
    data = {
        USERNAME: user.username,
        EMAIL: user.email,
        STUDENT_NUMBER: user.student_number,
        NUSNET_ID: user.nusnet_id,
        TELEGRAM_HANDLE: user.telegram_handle
    }
    return data

def get_user_with_nusnet_id(nusnet_id):
    try:
        return get_users(nusnet_id=nusnet_id).get()
    except User.DoesNotExist:
        return None

def get_user_with_student_number(student_number):
    try:
        return get_users(student_number=student_number).get()
    except User.DoesNotExist:
        return None
