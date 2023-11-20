from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Team, TeamInvitation
from .serializers import TeamSerializer, TeamInvitationSerializer
from users.models import User

from rest_framework import permissions
from rest_framework.exceptions import NotFound


class TeamCreateAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TeamSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            # Set the 'created_by' field to the current user
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeamInvitationCreateAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, team_id):
        try:
            team = Team.objects.get(id=team_id)
            # Ensure the user making the request is the team leader
            if team.created_by != request.user:
                raise PermissionDenied("You must be the team leader to invite members.")

            # Get the user to be invited
            invitee_username = request.data.get("username")
            invitee = User.objects.get(username=invitee_username)
            # Create the invitation
            invitation = TeamInvitation.objects.create(team=team, invitee=invitee)
            serializer = TeamInvitationSerializer(invitation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Team.DoesNotExist:
            return Response(
                {"error": "Team not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except User.DoesNotExist:
            return Response(
                {"error": "User to invite not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class IsTeamLeader(permissions.BasePermission):
    def has_permission(self, request, view):
        # `team_id`는 URL로부터 얻어옵니다.
        team_id = view.kwargs.get("team_id")
        try:
            team = Team.objects.get(id=team_id)
            # 팀 리더인지 확인합니다.
            return team.created_by == request.user
        except Team.DoesNotExist:
            return False


class TeamInvitationCreateAPIView(views.APIView):
    permission_classes = [IsAuthenticated, IsTeamLeader]

    def post(self, request, team_id):
        # IsTeamLeader 퍼미션에 의해 여기까지 도달했다면,
        # 요청자는 팀의 리더임이 보장됩니다.
        team = Team.objects.get(id=team_id)

        # 초대할 사용자를 가져옵니다.
        invitee_username = request.data.get("username")
        try:
            invitee = User.objects.get(username=invitee_username)
        except User.DoesNotExist:
            return Response(
                {"error": "User to invite not found."}, status=status.HTTP_404_NOT_FOUND
            )

        # 이미 초대된 사용자인지 확인합니다.
        if TeamInvitation.objects.filter(team=team, invitee=invitee).exists():
            return Response(
                {"error": "Invitation already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 초대를 생성합니다.
        invitation = TeamInvitation.objects.create(team=team, invitee=invitee)
        serializer = TeamInvitationSerializer(invitation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TeamInvitationAcceptAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, invitation_id):
        try:
            invitation = TeamInvitation.objects.get(
                id=invitation_id, invitee=request.user
            )

            # 초대가 pending 상태인지 확인합니다.
            if invitation.status != "pending":
                return Response(
                    {"error": "Invitation is already responded."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            invitation.status = "accepted"
            invitation.save()
            return Response(
                {"status": "Invitation accepted"}, status=status.HTTP_200_OK
            )

        except TeamInvitation.DoesNotExist:
            raise NotFound(detail="Invitation not found.")
