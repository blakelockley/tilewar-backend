from rest_framework.serializers import ModelSerializer

from tiles.models import Tile


class TileSerializer(ModelSerializer):
    class Meta:
        model = Tile
        fields = "__all__"
