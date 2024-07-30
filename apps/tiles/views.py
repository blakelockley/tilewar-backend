from rest_framework.views import APIView
from rest_framework.response import Response

from tiles.models import Tile
from tiles.serializers import TileSerializer


class TilesViews(APIView):

    def get(self, request, format=None):
        tiles = Tile.objects.all()

        serializer = TileSerializer(tiles, many=True)
        return Response(serializer.data)
