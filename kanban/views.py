from rest_framework import views, status, permissions
from rest_framework.response import Response
from .models import Column, KanbanBoard
from .serializers import ColumnSerializer
from teams.models import Team


class ColumnCreateAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, kanban_board_id):
        try:
            kanban_board = KanbanBoard.objects.get(pk=kanban_board_id)
            team = kanban_board.team
            if not team.created_teams.filter(created_by=request.user).exists():
                return Response(
                    {"error": "팀 리더만이 Column을 생성할 수 있습니다."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            if not team.team_invitations.filter(
                invitee=request.user, status="accepted"
            ).exists():
                return Response(
                    {"error": "팀 멤버가 아닙니다."}, status=status.HTTP_403_FORBIDDEN
                )

            serializer = ColumnSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(kanban_board=kanban_board)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except KanbanBoard.DoesNotExist:
            return Response(
                {"error": "칸반보드가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND
            )


class ColumnListView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, kanban_board_id):
        try:
            kanban_board = KanbanBoard.objects.get(pk=kanban_board_id)
            if not kanban_board.team.team_invitations.filter(
                invitee=request.user, status="accepted"
            ).exists():
                return Response(
                    {"error": "팀 멤버가 아닙니다."}, status=status.HTTP_403_FORBIDDEN
                )

            columns = Column.objects.filter(kanban_board_id=kanban_board_id).order_by(
                "order"
            )
            serializer = ColumnSerializer(columns, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except KanbanBoard.DoesNotExist:
            return Response(
                {"error": "칸반보드가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND
            )


class ColumnUpdateAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, column_id):
        try:
            column = Column.objects.get(pk=column_id)
            if not column.kanban_board.team.created_teams.filter(
                created_by=request.user
            ).exists():
                return Response(
                    {"error": "팀 리더만이 Column을 수정할 수 있습니다."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            serializer = ColumnSerializer(column, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Column.DoesNotExist:
            return Response(
                {"error": "Column이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND
            )


class ColumnDeleteAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, column_id):
        try:
            column = Column.objects.get(pk=column_id)
            if not column.kanban_board.team.created_teams.filter(
                created_by=request.user
            ).exists():
                return Response(
                    {"error": "팀 리더만이 Column을 삭제할 수 있습니다."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            column.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Column.DoesNotExist:
            return Response(
                {"error": "Column이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND
            )
