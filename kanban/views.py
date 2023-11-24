from rest_framework import views, status, permissions
from rest_framework.response import Response
from .models import Column, KanbanBoard, Ticket
from .serializers import ColumnSerializer, TicketSerializer


class IsTeamMember(permissions.BasePermission):
    """
    사용자가 지정된 팀의 멤버인지 확인하는 권한 클래스
    """

    def has_object_permission(self, request, view, obj):
        # obj는 Column 또는 Ticket의 인스턴스일 수 있음
        # 해당 객체의 칸반보드를 참조하여 팀을 확인
        team = (
            obj.kanban_board.team
            if hasattr(obj, "kanban_board")
            else obj.column.kanban_board.team
        )
        return team.team_invitations.filter(
            invitee=request.user, status="accepted"
        ).exists()


# 칸반보드의 Column 생성 API
class ColumnCreateAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    # POST 요청 처리
    def post(self, request, kanban_board_id):
        try:
            # 칸반보드 존재 확인
            kanban_board = KanbanBoard.objects.get(pk=kanban_board_id)
            team = kanban_board.team
            # 팀 리더 권한 확인
            if not team.created_teams.filter(created_by=request.user).exists():
                return Response(
                    {"error": "팀 리더만이 Column을 생성할 수 있습니다."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            # 팀 멤버 권한 확인
            if not team.team_invitations.filter(
                invitee=request.user, status="accepted"
            ).exists():
                return Response(
                    {"error": "팀 멤버가 아닙니다."}, status=status.HTTP_403_FORBIDDEN
                )
            # 데이터 유효성 검증 및 저장
            serializer = ColumnSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(kanban_board=kanban_board)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except KanbanBoard.DoesNotExist:
            return Response(
                {"error": "칸반보드가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND
            )


# 칸반보드의 Column 목록 조회 API
class ColumnListView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    # GET 요청 처리
    def get(self, request, kanban_board_id):
        try:
            # 칸반보드 존재 확인
            kanban_board = KanbanBoard.objects.get(pk=kanban_board_id)
            # 팀 멤버 권한 확인
            if not kanban_board.team.team_invitations.filter(
                invitee=request.user, status="accepted"
            ).exists():
                return Response(
                    {"error": "팀 멤버가 아닙니다."}, status=status.HTTP_403_FORBIDDEN
                )
            # Column 목록 조회 및 반환
            columns = Column.objects.filter(kanban_board_id=kanban_board_id).order_by(
                "order"
            )
            serializer = ColumnSerializer(columns, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except KanbanBoard.DoesNotExist:
            return Response(
                {"error": "칸반보드가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND
            )


# 칸반보드의 Column 수정 API
class ColumnUpdateAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    # PUT 요청 처리
    def put(self, request, column_id):
        try:
            # Column 존재 확인
            column = Column.objects.get(pk=column_id)
            # 팀 리더 권한 확인
            if not column.kanban_board.team.created_teams.filter(
                created_by=request.user
            ).exists():
                return Response(
                    {"error": "팀 리더만이 Column을 수정할 수 있습니다."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            # 데이터 유효성 검증 및 저장
            serializer = ColumnSerializer(column, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Column.DoesNotExist:
            return Response(
                {"error": "Column이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND
            )


# 칸반보드의 Column 삭제 API
class ColumnDeleteAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    # DELETE 요청 처리
    def delete(self, request, column_id):
        try:
            # Column 존재 확인
            column = Column.objects.get(pk=column_id)
            # 팀 리더 권한 확인
            if not column.kanban_board.team.created_teams.filter(
                created_by=request.user
            ).exists():
                return Response(
                    {"error": "팀 리더만이 Column을 삭제할 수 있습니다."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            # Column 삭제
            column.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Column.DoesNotExist:
            return Response(
                {"error": "Column이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND
            )


# 칸반 Column 순서 변경 API
class ColumnOrderUpdateAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    # PUT 요청 처리 (Column 순서 변경)
    def put(self, request, kanban_board_id):
        try:
            # 칸반보드 존재 확인
            kanban_board = KanbanBoard.objects.get(pk=kanban_board_id)
            # 팀 리더 권한 확인
            if not kanban_board.team.created_teams.filter(
                created_by=request.user
            ).exists():
                return Response(
                    {"error": "팀 리더만이 Column의 순서를 변경할 수 있습니다."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            # 요청 데이터에서 Column의 새 순서를 가져옴
            new_order = request.data.get("order")
            if not isinstance(new_order, list):
                return Response(
                    {"error": "잘못된 데이터 형식입니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # Column의 순서 업데이트
            for index, column_id in enumerate(new_order):
                Column.objects.filter(pk=column_id, kanban_board=kanban_board).update(
                    order=index
                )
            return Response(
                {"message": "Column 순서가 업데이트 되었습니다."}, status=status.HTTP_200_OK
            )
        except KanbanBoard.DoesNotExist:
            return Response(
                {"error": "칸반보드가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND
            )


# 칸반보드의 Ticket 생성 API
class TicketCreateAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsTeamMember]

    def post(self, request, column_id):
        try:
            column = Column.objects.get(pk=column_id)
            serializer = TicketSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(column=column)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Column.DoesNotExist:
            return Response(
                {"error": "Column이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND
            )


# 칸반보드의 Ticket 수정 API
class TicketUpdateAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsTeamMember]

    def put(self, request, ticket_id):
        try:
            ticket = Ticket.objects.get(pk=ticket_id)
            if not IsTeamMember(request.user, ticket.column.kanban_board.team):
                return Response(
                    {"error": "팀 멤버가 아닙니다."}, status=status.HTTP_403_FORBIDDEN
                )

            serializer = TicketSerializer(ticket, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Ticket.DoesNotExist:
            return Response(
                {"error": "해당 ID의 Ticket이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND
            )


# 칸반보드의 Ticket 삭제 API
class TicketDeleteAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsTeamMember]

    def delete(self, request, ticket_id):
        try:
            ticket = Ticket.objects.get(pk=ticket_id)
            if not IsTeamMember(request.user, ticket.column.kanban_board.team):
                return Response(
                    {"error": "팀 멤버가 아닙니다."}, status=status.HTTP_403_FORBIDDEN
                )

            ticket.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Ticket.DoesNotExist:
            return Response(
                {"error": "해당 ID의 Ticket이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND
            )


class TicketOrderUpdateAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, column_id):
        try:
            column = Column.objects.get(pk=column_id)
            new_order = request.data.get("order")
            if not isinstance(new_order, list):
                return Response(
                    {"error": "잘못된 데이터 형식입니다."}, status=status.HTTP_400_BAD_REQUEST
                )

            for index, ticket_id in enumerate(new_order):
                Ticket.objects.filter(pk=ticket_id, column=column).update(order=index)

            return Response(
                {"message": "Ticket 순서가 업데이트 되었습니다."}, status=status.HTTP_200_OK
            )
        except Column.DoesNotExist:
            return Response(
                {"error": "Column이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND
            )


# 칸반 Ticket Column 이동 API
class TicketColumnMoveAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsTeamMember]

    def put(self, request, ticket_id):
        try:
            ticket = Ticket.objects.get(pk=ticket_id)
            new_column_id = request.data.get("new_column_id")

            new_column = Column.objects.get(pk=new_column_id)
            if not IsTeamMember(request.user, new_column.kanban_board.team):
                return Response(
                    {"error": "팀 멤버가 아닙니다."}, status=status.HTTP_403_FORBIDDEN
                )

            ticket.column = new_column
            ticket.save()
            return Response(
                {"message": "Ticket이 새 Column으로 이동되었습니다."}, status=status.HTTP_200_OK
            )
        except Ticket.DoesNotExist:
            return Response(
                {"error": "해당 ID의 Ticket이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND
            )
        except Column.DoesNotExist:
            return Response(
                {"error": "해당 ID의 Column이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND
            )
