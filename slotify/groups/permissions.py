from rest_framework.permissions import (
    BasePermission,
)
from .methods import is_group_admin

class GroupAdminPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        group = view.get_object()
        return is_group_admin(request.user, group)

class MembershipGroupAdminPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        group = view.get_object().group
        return is_group_admin(request.user, group)

class EventGroupAdminPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        event = view.get_object()
        group = event.group
        return is_group_admin(request.user, group)