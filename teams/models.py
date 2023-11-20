from django.db import models
from users.models import User


class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_by = models.ForeignKey(
        "users.User", related_name="created_teams", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class TeamInvitation(models.Model):
    team = models.ForeignKey(
        "Team", on_delete=models.CASCADE, related_name="invitations"
    )
    invitee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="team_invitations"
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("accepted", "Accepted"),
            ("declined", "Declined"),
        ],
        default="pending",
    )

    def __str__(self):
        return f"{self.team.name} - {self.invitee.username} - {self.status}"
