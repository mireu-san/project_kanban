from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from kanban.models import Ticket, Column
from users.models import User
from django.db.models import Count, Avg, F
from datetime import datetime, timedelta


class WorkAnalysisAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 특정 기간 (예: 최근 30일) 설정
        days = int(request.query_params.get("days", 30))
        start_date = datetime.now() - timedelta(days=days)

        # Ticket 데이터 분석
        analysis_data = (
            Ticket.objects.filter(
                column__kanban_board__team__team_invitations__invitee=request.user,
                column__kanban_board__team__team_invitations__status="accepted",
                created_at__gte=start_date,
            )
            .values(
                "column__kanban_board__team__name",
                assignee=F("column__kanban_board__team__created_by__username"),
            )
            .annotate(
                total_tickets=Count("id"),
                completed_tickets=Count("id", filter=F("status") == "completed"),
            )
        )

        return Response(analysis_data)


class TeamMemberComparisonAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        team_id = request.query_params.get("team_id")
        if not team_id:
            return Response({"error": "Analyst: Team ID 가 감지되지 않는 것 같습니다."}, status=400)

        # 팀원별 작업 데이터 비교
        comparison_data = (
            User.objects.filter(
                team_invitations__team_id=team_id, team_invitations__status="accepted"
            )
            .annotate(
                total_tickets=Count("created_teams__kanban_boards__columns__tickets"),
                completed_tickets=Count(
                    "created_teams__kanban_boards__columns__tickets",
                    filter=F("tickets__status") == "completed",
                ),
            )
            .values("username", "total_tickets", "completed_tickets")
        )

        return Response(comparison_data)
