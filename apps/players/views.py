from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Player, Team


class WhoAmIView(APIView):
    def get(self, request: Request, format=None):

        if player := Player.get_from_request(request):
            return Response({"username": player.username})

        return Response(status=401)


class TeamsView(APIView):
    def get(self, request: Request, format=None):

        teams = list[dict[str, str]]()

        for team in Team.objects.all():
            teams.append(
                {
                    "name": team.name,
                    "colour": team.colour,
                    "players": map(
                        lambda p: {"id": p.id, "username": p.username},
                        team.player_set.all(),
                    ),
                    "completed_tiles": team.tile_set.filter(
                        completed_by_team=team
                    ).count(),
                }
            )

        return Response(teams)
