from django.urls import path
from .views import TeamCreateAPIView

urlpatterns = [
    path("create/", TeamCreateAPIView.as_view(), name="team-create"),
]
