from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_by = models.ForeignKey(
        "users.User", related_name="created_teams", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
