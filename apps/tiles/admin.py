from django.contrib import admin

from tiles.models import Task, Tile


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "difficulty",
    )


@admin.register(Tile)
class TileAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "index",
        "task",
        "visible_to_all",
        "starting_tile_for_team",
        "completed_by_team",
    )

    list_editable = (
        "visible_to_all",
        "starting_tile_for_team",
        "completed_by_team",
    )
