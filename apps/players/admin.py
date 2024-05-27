from django.contrib import admin
from django.utils.html import mark_safe


from .models import Team, Player


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    search_fields = ("username",)

    list_display = (
        "username",
        "team",
        "access_token",
    )
    list_editable = ("team",)

    fields = (
        "username",
        "access_token",
        "team",
    )


class PlayerInline(admin.TabularInline):
    model = Player
    extra = 0

    fields = ("username",)
    readonly_fields = ("username",)

    def has_add_permission(self, request, obj):
        return False


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "number",
        "get_colour",
        "get_count",
    )

    fields = (
        "name",
        "number",
        "colour",
    )

    inlines = [PlayerInline]

    def get_count(self, obj):
        return obj.player_set.count()

    get_count.short_description = "Players"

    def get_colour(self, obj):
        return mark_safe(f'<span style="color: #{obj.colour}">#{obj.colour}</span>')

    get_colour.short_description = "Colour"
