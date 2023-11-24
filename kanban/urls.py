from django.urls import path
from .views import (
    ColumnCreateAPIView,
    ColumnListView,
    ColumnUpdateAPIView,
    ColumnDeleteAPIView,
    ColumnOrderUpdateAPIView,
    TicketCreateAPIView,
    TicketUpdateAPIView,
    TicketDeleteAPIView,
    TicketOrderUpdateAPIView,
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
    path("tickets/create/", TicketCreateAPIView.as_view(), name="ticket-create"),
    path(
        "tickets/<int:ticket_id>/", TicketUpdateAPIView.as_view(), name="ticket-update"
    ),
    path(
        "tickets/delete/<int:ticket_id>/",
        TicketDeleteAPIView.as_view(),
        name="ticket-delete",
    ),
    path(
        "tickets/order-update/<int:column_id>/",
        TicketOrderUpdateAPIView.as_view(),
        name="ticket-order-update",
    ),
]
