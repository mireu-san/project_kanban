from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, NotFound
from .models import Team, TeamInvitation
from .serializers import TeamSerializer, TeamInvitationSerializer
from users.models import User

# from rest_framework import permissions
from users.serializers import MyPageSerializer


class TeamCreateAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    # 팀 생성 API
    def post(self, request):
        serializer = TeamSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            # 생성자를 현재 사용자로 설정
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeamInvitationCreateAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    # 팀 초대 API
    def post(self, request, team_id):
        try:
            team = Team.objects.get(id=team_id)
            # 요청자가 팀 리더인지 확인
            if team.created_by != request.user:
                raise PermissionDenied("팀 리더만이 멤버를 초대할 수 있습니다.")

            # 초대할 사용자 가져오기
            invitee_username = request.data.get("username")
            invitee = User.objects.get(username=invitee_username)
            # 초대 생성
            invitation = TeamInvitation.objects.create(team=team, invitee=invitee)
            serializer = TeamInvitationSerializer(invitation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Team.DoesNotExist:
            return Response(
                {"error": "팀을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND
            )
        except User.DoesNotExist:
            return Response(
                {"error": "초대할 사용자를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TeamInvitationAcceptAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    # 초대 승낙 API
    def post(self, request, invitation_id):
        try:
            invitation = TeamInvitation.objects.get(
                id=invitation_id, invitee=request.user
            )

            # 초대가 대기 상태인지 확인
            if invitation.status != "pending":
                return Response(
                    {"error": "초대에 이미 응답되었습니다."}, status=status.HTTP_400_BAD_REQUEST
                )

            # 초대 상태를 'accepted'로 변경
            invitation.status = "accepted"
            invitation.save()
            return Response({"status": "초대가 승낙되었습니다."}, status=status.HTTP_200_OK)

        except TeamInvitation.DoesNotExist:
            raise NotFound(detail="초대를 찾을 수 없습니다.")


class TeamMemberListView(views.APIView):
    permission_classes = [IsAuthenticated]

    # 팀 멤버 목록 조회 API
    def get(self, request, team_id):
        try:
            team = Team.objects.get(id=team_id)
            # 팀의 수락된 초대 목록 가져오기
            invitations = TeamInvitation.objects.filter(team=team, status="accepted")
            members = [invitation.invitee for invitation in invitations]
            serializer = MyPageSerializer(members, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Team.DoesNotExist:
            return Response(
                {"error": "팀을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND
            )


class TeamInvitationRespondAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    # 초대 응답 API (승낙/거절)
    def post(self, request, invitation_id):
        response = request.data.get("response", "")  # 'accept' 또는 'decline'
        try:
            invitation = TeamInvitation.objects.get(
                id=invitation_id, invitee=request.user
            )

            if invitation.status != "pending":
                return Response(
                    {"error": "초대에 이미 응답되었습니다."}, status=status.HTTP_400_BAD_REQUEST
                )

            if response.lower() == "accept":
                invitation.status = "accepted"
            elif response.lower() == "decline":
                invitation.status = "declined"
            else:
                return Response(
                    {"error": "잘못된 응답입니다."}, status=status.HTTP_400_BAD_REQUEST
                )

            invitation.save()
            return Response(
                {"status": f"초대가 {response}되었습니다."}, status=status.HTTP_200_OK
            )

        except TeamInvitation.DoesNotExist:
            raise NotFound(detail="초대를 찾을 수 없습니다.")
