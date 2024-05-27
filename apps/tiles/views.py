from typing import Any
from django.shortcuts import render

from players.models import Player
from rest_framework.views import APIView
from rest_framework.response import Response

from tiles.models import Tile


class TilesViews(APIView):

    def get(self, request, format=None):
        try:
            player = Player.get_from_request(request)
        except:
            player = None

        tiles = list[dict[str, Any]]()

        for tile in Tile.objects.all():
            if tile.completed_by_team:
                tiles.append(
                    {
                        "index": tile.index,
                        "number": tile.index + 1,
                        "task": {
                            "title": tile.task.title,
                            "category": tile.task.category,
                            "difficulty": tile.task.difficulty,
                        },
                        "completed_by_team": {
                            "number": tile.completed_by_team.number,
                            "name": tile.completed_by_team.name,
                            "colour": tile.completed_by_team.colour,
                        },
                        "visible_to_teams": tile.visible_to_teams,
                    }
                )

                continue

            if tile.is_visible_to_player(player):
                tiles.append(
                    {
                        "index": tile.index,
                        "number": tile.index + 1,
                        "task": {
                            "title": tile.task.title,
                            "category": tile.task.category,
                            "difficulty": tile.task.difficulty,
                        },
                        "completed_by": None,
                        "visible_to_teams": tile.visible_to_teams,
                    }
                )

            else:
                tiles.append(
                    {
                        "index": tile.index,
                        "number": tile.index + 1,
                        "task": None,
                        "completed": False,
                        "completed_by_team": None,
                        "visible_to_teams": tile.visible_to_teams,
                    }
                )

        return Response(tiles)
