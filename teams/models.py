from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

PLAYING_STATES = {
    'on_the_court': 0,
    'on_the_bench': 4,
    'gone_home': 8,
}


PLAYING_STATE_CHOICES = [
    (val, key.replace('_', ' ').capitalize())
    for key, val in PLAYING_STATES.items()
]


class Team(models.Model):
    name = models.CharField(max_length=50, unique=True)
    managers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('teams:detail', args=[str(self.id)])


class Player(models.Model):
    name = models.CharField(max_length=50)
    team = models.ForeignKey(Team)
    score = models.FloatField()
    state = models.IntegerField(max_length=2,
                                choices=PLAYING_STATE_CHOICES,
                                default=PLAYING_STATES['gone_home'])

    class Meta:
        unique_together = ('team', 'name')
        ordering = ('state', 'name')
