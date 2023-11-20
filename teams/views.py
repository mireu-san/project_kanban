from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Team
from .serializers import TeamSerializer


class TeamCreateAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TeamSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            # Set the 'created_by' field to the current user
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
