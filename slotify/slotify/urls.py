from django.contrib import admin
from django.urls import path, include

API_PREFIX = "api/v1"

urlpatterns = [
    path("admin/", include("admin_honeypot.urls", namespace="admin_honeypot")),
    path("not_admin/", admin.site.urls),
    path("auth/", include("authentication.urls")),
    path(f"{API_PREFIX}/groups/", include("groups.urls")),
]
