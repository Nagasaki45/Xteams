from django import forms

from .models import Player
from . import grouper


class GameForm(forms.Form):
    num_of_groups = forms.IntegerField(min_value=2, initial=2)
    chance_widget = forms.NumberInput(attrs={'type': 'range'})
    chance_text = 'low chance value will create ' + \
                  'groups with similar ability (recommended).'
    chance = forms.FloatField(min_value=grouper.MIN_CHANCE,
                              max_value=1,
                              widget=chance_widget,
                              help_text=chance_text,
                              initial=grouper.DEFAULT_CHANCE)
    