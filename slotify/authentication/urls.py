from django.urls import path
from .views import RegisterView, VerifyEmailView, LoginView, UserProfileView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('verify-email/', VerifyEmailView.as_view(), name="verify-email"),
    path('token-refresh', TokenRefreshView.as_view(), name="token-refresh"),
    path('profile', UserProfileView.as_view(), name="user-profile")
]