from rest_framework.exceptions import AuthenticationFailed, PermissionDenied

from authentication.models import User
from authentication.methods import get_users

def check_requester_is_authenticated():
    def _method_wrapper(view_method):
        def _arguments_wrapper(instance, request, *args, **kwargs):
            requester_id = request.user.id

            try:
                requester = get_users(id=requester_id).get()

            except User.DoesNotExist as e:
                raise AuthenticationFailed(
                    detail="Invalid user.",
                    code="invalid_user",
                )

            return view_method(instance, request, requester=requester, *args, **kwargs)

        return _arguments_wrapper

    return _method_wrapper