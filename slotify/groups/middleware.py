from authentication.models import User
from rest_framework.exceptions import NotFound, PermissionDenied

from .models import Group, Membership
from .methods import get_groups, get_memberships

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
           raise NotFound(detail="No group found", code="no_group_found")


        return view_method(
            instance, request, requester=requester, group=group, *args, **kwargs
        )

    return _arguments_wrapper

def check_requester_is_group_admin(view_method):
    def _arguments_wrapper(
        instance, request, requester: User, group: Group, *args, **kwargs
    ):
        try:
            membership = (
                get_memberships(group=group, user=requester)
                .get()
            )
        except (Membership.DoesNotExist):
            raise PermissionDenied(detail="Not group member", code="not_group_member")

        if not membership.is_approved or not membership.is_admin:
            raise PermissionDenied(detail="Not group admin", code="not_group_admin")

        return view_method(
            instance, request, requester=requester, group=group, *args, **kwargs
        )

    
    return _arguments_wrapper
