from .models import User, Profile
from common.constants import USERNAME, EMAIL, TELEGRAM_HANDLE, STUDENT_NUMBER, NUSNET_ID

def get_users(*args, **kwargs):
    return User.objects.filter(*args, **kwargs)

def get_profiles(*args, **kwargs):
    return Profile.objects.filter(*args, **kwargs)

def user_to_json(user):
    user_data = {
        USERNAME: user.username,
        EMAIL: user.email,
    }

    profile = user.profile if hasattr(user, 'profile') else None
    profile_data = profile_to_json(profile)
    user_data.update(profile_data)

    return user_data

def profile_to_json(profile):
    profile_data = {
        STUDENT_NUMBER: profile.student_number if profile else "",
        NUSNET_ID: profile.nusnet_id if profile else "",
        TELEGRAM_HANDLE: profile.telegram_handle if profile else ""
    }
    return profile_data

def get_user_with_nusnet_id(nusnet_id):
    try:
        profile = get_profiles(nusnet_id=nusnet_id).get()
        return profile.user
    except Profile.DoesNotExist:
        return None

def get_user_with_student_number(student_number):
    try:
        profile = get_profiles(student_number=student_number).get()
        return profile.user
    except Profile.DoesNotExist:
        return None

def get_user_by_email(email):
    try:
        return (
            get_users(email=email)
            .select_related('profile')
            .get()
        )
    except User.DoesNotExist:
        return None

def check_if_other_user_with_field_exists(fetch_user_by_field_function, field_value, user) -> True:
    fetched_user = fetch_user_by_field_function(field_value)
    return fetched_user and fetched_user != user