import uuid
from typing import Any, Optional

from django.db import models
from django.utils.translation import ugettext_lazy as _

from players.models import Player, Team


class Category(models.TextChoices):
    PVM = "PVM", "PVM"
    SKILLING = "SKILLING", "Skilling"
    COLLECTION_LOG = "COLLECTION_LOG", "Collection Log"
    OTHER = "OTHER", "Other"


class Difficulty(models.TextChoices):
    EASY = "EASY", "Easy"
    MEDIUM = "MEDIUM", "Medium"
    HARD = "HARD", "Hard"


class Task(models.Model):
    class Meta:
        ordering = ("title",)

    title = models.CharField(max_length=100)
    description = models.TextField()

    category = models.CharField(
        max_length=20, choices=Category.choices, default=Category.OTHER
    )
    difficulty = models.CharField(
        max_length=20, choices=Difficulty.choices, default=Difficulty.EASY
    )

    image = models.ImageField(upload_to="tasks", blank=True, null=True)

    def __str__(self):
        return f"Task ({self.title})"


class Tile(models.Model):
    class Meta:
        ordering = ("index",)

    index = models.PositiveIntegerField(unique=True)

    task = models.ForeignKey(Task, null=True, on_delete=models.SET_NULL)

    visible_to_all = models.BooleanField(default=False)
    starting_tile_for_team = models.ForeignKey(
        "players.Team",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="starting_tile",
    )

    completed_by_team = models.ForeignKey(
        "players.Team",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    completed_by_player = models.ForeignKey(
        "players.Player",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Tile ({self.index}. {self.task.title})"

    def _get_adjacent_tile(self):
        adjacent_tile_numbers = set()

        row = (self.index) // 10
        col = (self.index) % 10

        if row > 0:
            # above
            adjacent_tile_numbers.add((row - 1) * 10 + col)

            if col > 0:  # above left
                adjacent_tile_numbers.add((row - 1) * 10 + col - 1)

            if col < 9:  # above right
                adjacent_tile_numbers.add((row - 1) * 10 + col + 1)

        if row < 9:  # below
            adjacent_tile_numbers.add((row + 1) * 10 + col)

            if col > 0:  # below left
                adjacent_tile_numbers.add((row + 1) * 10 + col - 1)

            if col < 9:  # below right
                adjacent_tile_numbers.add((row + 1) * 10 + col + 1)

        if col > 0:  # left
            adjacent_tile_numbers.add(row * 10 + col - 1)

        if col < 9:  # right
            adjacent_tile_numbers.add(row * 10 + col + 1)

        return Tile.objects.filter(index__in=adjacent_tile_numbers)

    def is_visible_to_player(self, player: Optional[Player]):
        if self.visible_to_all or self.completed_by_team:
            return True

        if player is None or not hasattr(player, "team"):
            return False

        adjacent_tiles = self._get_adjacent_tile()
        return adjacent_tiles.filter(completed_by_team=player.team).exists()

    @property
    def visible_to_teams(self):
        adjacent_tiles = self._get_adjacent_tile()
        teams = list[dict[str, Any]]()

        for team in Team.objects.all():
            if team == self.starting_tile_for_team:
                teams.append(
                    {"number": team.number, "name": team.name, "colour": team.colour}
                )

            if adjacent_tiles.filter(completed_by_team=team).exists():
                teams.append(
                    {"number": team.number, "name": team.name, "colour": team.colour}
                )

        # TODO: Remove duplicates

        return list(teams)
