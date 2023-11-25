from django.urls import path
from .views import WorkAnalysisAPIView, TeamMemberComparisonAPIView

urlpatterns = [
    path("work-analysis/", WorkAnalysisAPIView.as_view(), name="work-analysis"),
    path(
        "team-member-comparison/",
        TeamMemberComparisonAPIView.as_view(),
        name="team-member-comparison",
    ),
]
