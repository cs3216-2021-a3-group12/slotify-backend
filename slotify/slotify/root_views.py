from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "register": reverse("register", request=request, format=format),
            "login": reverse("login", request=request, format=format),
            "verify email": reverse("verify-email", request=request, format=format),
            "list of groups": reverse("groups-list", request=request, format=format),
            "create new group": reverse(
                "groups-create", request=request, format=format
            ),
            "group details": reverse(
                "groups-detail", request=request, format=format, args="1"
            ),
            "list of tags": reverse("tags-list", request=request, format=format),
            "create new tag": reverse("tags-create", request=request, format=format),
            "tag details": reverse(
                "tags-detail", request=request, format=format, args="1"
            ),
            "list of categories": reverse(
                "categories-list", request=request, format=format
            ),
            "create new category": reverse(
                "categories-create", request=request, format=format
            ),
            "category details": reverse(
                "categories-detail", request=request, format=format, args="1"
            ),
            "list of members": reverse("members-list", request=request, format=format),
            "list pf memberships records for a group": reverse(
                "memberships-list", request=request, format=format, args="1"
            ),
            "create new membership": reverse(
                "memberships-create", request=request, format=format
            ),
            "membership details": reverse(
                "memberships-detail", request=request, format=format, args="1"
            ),
            "list of events": reverse("events-list", request=request, format=format),
            "create new event": reverse(
                "group-events", request=request, format=format, args="1"
            ),
            "event details": reverse(
                "events-detail", request=request, format=format, args="1"
            ),
        }
    )
