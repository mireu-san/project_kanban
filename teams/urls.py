from django.urls import path
from .views import (
    TeamCreateAPIView,
    TeamInvitationCreateAPIView,
    TeamInvitationAcceptAPIView,
)

urlpatterns = [
    path("create/", TeamCreateAPIView.as_view(), name="team-create"),
    path(
        "<int:team_id>/invite/",
        TeamInvitationCreateAPIView.as_view(),
        name="team-invite",
    ),
    path(
        "invitations/<int:invitation_id>/accept/",
        TeamInvitationAcceptAPIView.as_view(),
        name="invitation-accept",
    ),
]
