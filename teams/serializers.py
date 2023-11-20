from rest_framework import serializers
from .models import Team, TeamInvitation


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["id", "name", "created_by"]
        read_only_fields = ["id", "created_by"]


class TeamInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamInvitation
        fields = ["id", "team", "invitee", "status"]
        read_only_fields = ["id", "status"]
