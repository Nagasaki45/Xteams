# Xteams! Sport teams management utility
# Copyright (C) 2014  Tom Gurion

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
    state = models.IntegerField(choices=PLAYING_STATE_CHOICES,
                                default=PLAYING_STATES['gone_home'])

    class Meta:
        unique_together = ('team', 'name')
        ordering = ('state', 'name')
