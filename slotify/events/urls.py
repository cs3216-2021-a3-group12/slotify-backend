from django.urls import path

from .views import EventListView, EventRetrieveUpdateDestroy
from events.api_views.sign_ups_views import (
    SlotsView, SingleSlotView, PostDeleteSignUpView, AdminGetSignUpsView, AdminUpdateSignUpsView
)

urlpatterns = [
    path('', EventListView.as_view(), name="events-list"),
    path('<int:id>/', EventRetrieveUpdateDestroy.as_view(), name="events-detail"),
    path('<int:event_id>/slots', SlotsView.as_view(), name="event-slots-list"),
    path('slots/<int:slot_id>', SingleSlotView.as_view(), name="single-slot-view"),
    path('slots/<int:slot_id>/signups', PostDeleteSignUpView.as_view(), name="signup-post-delete"),
    path('<int:event_id>/admin/signups', AdminGetSignUpsView.as_view(), name="signup-admin-view"),
    path('admin/signups/<int:signup_id>', AdminUpdateSignUpsView.as_view(), name="signup-admin-put")
]