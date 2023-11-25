from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from kanban.models import Ticket
from django.db.models import Sum
from datetime import datetime, timedelta


class WorkAnalysisAPIView(APIView):
    """
    사용자별 작업 분석을 위한 API 뷰입니다.
    'kanban' 앱의 티켓 정보와 'users' 앱을 이용하여 사용자별 데이터를 가져옵니다.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.query_params.get("user_id")
        columns = request.query_params.getlist("columns")
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        query = Ticket.objects.filter(
            column__kanban_board__team__team_invitations__invitee=request.user,
            column__kanban_board__team__team_invitations__status="accepted",
        )

        if user_id:
            query = query.filter(assignee_id=user_id)
        if columns:
            query = query.filter(column_id__in=columns)
        if start_date and end_date:
            query = query.filter(deadline__range=[start_date, end_date])

        analysis_data = (
            query.values("tag")
            .annotate(total_work_time=Sum("work_time"))
            .order_by("-total_work_time")  # 해당 필드 값 내림차순으로 정렬
        )

        total_time = sum(item["total_work_time"] for item in analysis_data)
        for item in analysis_data:
            item["percentage"] = (
                (item["total_work_time"] / total_time) * 100 if total_time else 0
            )

        return Response(analysis_data)


class TeamMemberComparisonAPIView(APIView):
    """
    팀원별 작업 기여도 비교를 위한 API 뷰입니다.
    'kanban', 'teams', 'users' 앱의 데이터를 통합하여 사용합니다.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        team_id = request.query_params.get("team_id")
        columns = request.query_params.getlist("columns")
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        tag = request.query_params.get("tag")

        if not team_id:
            return Response(
                {"error": "Team ID 가 필요합니다. Analyst 에서 감지하지 못하는 것 같습니다."}, status=400
            )

        query = Ticket.objects.filter(column__kanban_board__team_id=team_id)

        if columns:
            query = query.filter(column_id__in=columns)
        if start_date and end_date:
            query = query.filter(deadline__range=[start_date, end_date])
        if tag:
            query = query.filter(tag=tag)

        comparison_data = (
            query.values("assignee__username")
            .annotate(total_work_time=Sum("work_time"))
            .order_by("-total_work_time")  # 해당 필드 값 내림차순으로 정렬
        )

        total_time = sum(item["total_work_time"] for item in comparison_data)
        average_time = total_time / len(comparison_data) if comparison_data else 0

        for item in comparison_data:
            item["contribution"] = (
                (item["total_work_time"] / average_time) if average_time else 0
            )

        return Response(comparison_data)
