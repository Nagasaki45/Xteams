from django.db import models

from teams.models import Team


class TelegramGroup(models.Model):
    group = models.ForeignKey(Team)
    chat_id = models.IntegerField()
