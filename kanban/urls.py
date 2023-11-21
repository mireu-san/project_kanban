from django.urls import path
from .views import (
    ColumnCreateAPIView,
    ColumnListView,
    ColumnUpdateAPIView,
    ColumnDeleteAPIView,
)

urlpatterns = [
    path("columns/create/", ColumnCreateAPIView.as_view(), name="column-create"),
    path("columns/", ColumnListView.as_view(), name="column-list"),
    path(
        "columns/<int:column_id>/", ColumnUpdateAPIView.as_view(), name="column-update"
    ),
    path(
        "columns/delete/<int:column_id>/",
        ColumnDeleteAPIView.as_view(),
        name="column-delete",
    ),
]
