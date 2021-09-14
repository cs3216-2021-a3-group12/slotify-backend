from authentication.models import User
from rest_framework.exceptions import NotFound

from .models import Group
from .methods import get_groups

def check_group_exists(view_method):
    def _arguments_wrapper(
        instance, request, requester: User, group_id: int, *args, **kwargs
    ):

        try:
            group = (
                get_groups(id=group_id)
                .select_related("category")
                .get()
            )
        except (Group.DoesNotExist):
           raise NotFound(detail="No group found", code="no_group_cound")


        return view_method(
            instance, request, requester=requester, group=group, *args, **kwargs
        )

    return _arguments_wrapper

# def check_requester_is_group_admin(view_method):
#     def _arguments_wrapper(
#         instance, request, requester: User, group: Group, *args, **kwargs
#     )
