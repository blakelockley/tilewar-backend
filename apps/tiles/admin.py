from django.contrib import admin

from tiles.models import Tile


@admin.register(Tile)
class TileAdmin(admin.ModelAdmin):
    pass
