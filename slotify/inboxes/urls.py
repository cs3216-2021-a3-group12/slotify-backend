from django.urls import path

from .api_views import MessageListView, MessageCreateView, MessageUpdateView

urlpatterns = [
    path('', MessageListView.as_view(), name="messages-list"),
    path('new/', MessageCreateView.as_view(), name="messages-create"),
    path('<int:id>/', MessageUpdateView.as_view(), name="messages-update")
]