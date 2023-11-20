from django.urls import path
from .views import (
    TeamCreateAPIView,
    TeamInvitationCreateAPIView,
    TeamInvitationAcceptAPIView,
    TeamMemberListView,
    TeamInvitationRespondAPIView,
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
    path(
        "team/<int:team_id>/members/",
        TeamMemberListView.as_view(),
        name="team-members-list",
    ),
    path(
        "invitations/<int:invitation_id>/respond/",
        TeamInvitationRespondAPIView.as_view(),
        name="invitation-respond",
    ),
]
