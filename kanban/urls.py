from django.urls import path
from .views import (
    ColumnCreateAPIView,
    ColumnListView,
    ColumnUpdateAPIView,
    ColumnDeleteAPIView,
    ColumnOrderUpdateAPIView,
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
    path(
        "kanban-board/<int:kanban_board_id>/columns/order/",
        ColumnOrderUpdateAPIView.as_view(),
        name="column-order-update",
    ),
]
