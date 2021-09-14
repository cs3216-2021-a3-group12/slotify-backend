from django.urls import path

from .views import EventsView

urlpatterns = [
    path('', EventsView.as_view(), name="events")
]