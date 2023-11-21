from django.db import models
from teams.models import Team


class KanbanBoard(models.Model):
    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="kanban_boards"
    )

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Column(models.Model):
    kanban_board = models.ForeignKey(
        KanbanBoard, on_delete=models.CASCADE, related_name="columns"
    )

    name = models.CharField(max_length=255)
    order = models.IntegerField()

    def __str__(self):
        return self.name
