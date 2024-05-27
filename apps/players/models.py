from secrets import token_hex
from typing import Optional

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Team(models.Model):
    class Meta:
        ordering = ("number",)

    # TODO: Make unique
    number = models.PositiveIntegerField()

    name = models.CharField(max_length=40)
    colour = models.CharField(max_length=10, default="000000")

    def __str__(self):
        return f"Team ({self.name})"


class Player(models.Model):
    username = models.CharField(max_length=20, unique=True)
    access_token = models.CharField(max_length=32, unique=True, blank=True)

    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.access_token:
            self.access_token = token_hex(16)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Player ({self.username})"

    @classmethod
    def get_from_request(cls, request) -> Optional["Player"]:
        try:
            access_token = request.headers.get("Authorization")
            return cls.objects.get(access_token=access_token)
        except:
            return None
