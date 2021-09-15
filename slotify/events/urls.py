from django.urls import path

from .views import EventListView, EventRetrieveUpdateDestroy

urlpatterns = [
    path('', EventListView.as_view(), name="events-list"),
    path('<int:id>/', EventRetrieveUpdateDestroy.as_view(), name="events-detail")
]