from django.urls import path
from .views import TeamCreateAPIView, TeamInvitationCreateAPIView

urlpatterns = [
    path("create/", TeamCreateAPIView.as_view(), name="team-create"),
    path(
        "<int:team_id>/invite/",
        TeamInvitationCreateAPIView.as_view(),
        name="team-invite",
    ),
]
