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


class Ticket(models.Model):
    column = models.ForeignKey(Column, on_delete=models.CASCADE, related_name="tickets")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    order = models.IntegerField()
    work_time = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    tag = models.CharField(max_length=100, blank=True, null=True)
    deadline = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title
