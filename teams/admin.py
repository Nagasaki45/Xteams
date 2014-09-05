from django.contrib import admin

from .models import Team, Player


class PlayerInline(admin.TabularInline):
    model = Player
    fields = ['name', 'score']
    extra = 3


class TeamAdmin(admin.ModelAdmin):
    fields = ['name', 'managers']
    inlines = [PlayerInline]


admin.site.register(Team, TeamAdmin)
