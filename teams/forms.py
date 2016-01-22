from django import forms

from .models import Player
from . import grouper


class GameForm(forms.Form):
    num_of_teams = forms.IntegerField(min_value=2, initial=2)
