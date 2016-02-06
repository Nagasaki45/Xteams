from django.contrib import admin

from .models import Group, Player


class PlayerInline(admin.TabularInline):
    model = Player
    fields = ['name', 'score']
    extra = 3


class GroupAdmin(admin.ModelAdmin):
    fields = ['name', 'managers']
    inlines = [PlayerInline]


admin.site.register(Group, GroupAdmin)
