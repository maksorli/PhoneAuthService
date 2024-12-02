# app/users/urls.py
from django.urls import path

from .views import ActivateInviteCodeView, SendCodeView, UserProfileView, VerifyCodeView

urlpatterns = [
    path("send-code/", SendCodeView.as_view(), name="send_code"),
    path("verify-code/", VerifyCodeView.as_view(), name="verify_code"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("activate-invite/", ActivateInviteCodeView.as_view(), name="activate_invite"),
]
