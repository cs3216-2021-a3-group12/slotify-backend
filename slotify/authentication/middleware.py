from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from authentication.models import User
from authentication.methods import get_users
from common.constants import MESSAGE

def check_requester_is_authenticated(view_method):
    def _arguments_wrapper(instance, request, *args, **kwargs):
        requester_id = request.user.id

        try:
            requester = (
                get_users(id=requester_id)
                .select_related("profile")
                .get()
            )
        except User.DoesNotExist as e:
            raise AuthenticationFailed(
                detail="Invalid user.",
                code="invalid_user",
            )

        return view_method(instance, request, requester=requester, *args, **kwargs)

    return _arguments_wrapper

def check_requester_has_profile(view_method):
    def _arguments_wrapper(instance, request, requester, *args, **kwargs):
        if not hasattr(requester, "profile"):
            return Response(
                {MESSAGE: "User profile information required. Please fill in before proceeding."},
                status=452
            )

        return view_method(instance, request, requester=requester, *args, **kwargs)

    return _arguments_wrapper