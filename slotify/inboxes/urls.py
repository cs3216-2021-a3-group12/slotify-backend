from django.urls import path

from .api_views import MessageListView, MessageUpdateView

urlpatterns = [
    path('', MessageListView.as_view(), name="messages-list"),
    path('<int:id>/', MessageUpdateView.as_view(), name="messages-update")
]