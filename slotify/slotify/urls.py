from django.contrib import admin
from django.urls import path, include
from .root_views import api_root

API_PREFIX = "api/v1"

urlpatterns = [
    path("", api_root, name="api-root"),
    path("admin/", include("admin_honeypot.urls", namespace="admin_honeypot")),
    path("not_admin/", admin.site.urls),
    path("auth/", include("authentication.urls")),
    path(f"{API_PREFIX}/groups/", include("groups.urls")),
    path(f"{API_PREFIX}/events/", include("events.urls")),
    path(f"{API_PREFIX}/messages/", include("inboxes.urls")),
    path('social_auth/', include(('social_auth.urls', 'social_auth'), namespace="social_auth")),
]
