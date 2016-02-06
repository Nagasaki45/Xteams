from django import forms

from .models import Player
from . import grouper


class GameForm(forms.Form):
    number_of_teams = forms.IntegerField(min_value=2, initial=2)

    def __init__(self, *args, **kwargs):
        try:
            self.num_of_players = kwargs.pop('num_of_players')
        except KeyError:
            pass
        return super().__init__(*args, **kwargs)

    def clean_number_of_teams(self):
        if self.cleaned_data['number_of_teams'] > self.num_of_players:
            raise forms.ValidationError('Not enough players to create teams.')
        return self.cleaned_data['number_of_teams']
