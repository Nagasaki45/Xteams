from django.db import models
from django.conf import settings
from django.urls import reverse

PLAYING_STATE_CHOICES = [
    (0, 'On the court'),
    (4, 'On the bench'),
    (8, 'Gone home'),
]
NUM_TO_PLAYING_STATE = {num: state.lower().replace(' ', '_') for num, state in PLAYING_STATE_CHOICES}
PLAYING_STATE_TO_NUM = {state.lower().replace(' ', '_'): num for num, state in PLAYING_STATE_CHOICES}


class Group(models.Model):
    name = models.CharField(max_length=50, unique=True)
    managers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('groups:detail', args=[str(self.id)])


class Player(models.Model):
    name = models.CharField(max_length=50)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    score = models.FloatField()
    state = models.IntegerField(choices=PLAYING_STATE_CHOICES,
                                default=PLAYING_STATE_TO_NUM['gone_home'])

    class Meta:
        unique_together = ['group', 'name']
        ordering = ['name']

    @property
    def state_name(self):
        return NUM_TO_PLAYING_STATE[self.state]

    @state_name.setter
    def state_name(self, value):
        self.state = PLAYING_STATE_TO_NUM[value]
