from django.contrib import messages

from .models import PLAYING_STATE_TO_NUM


def get_group_players(team, state):
    return list(team.player_set.filter(state=PLAYING_STATE_TO_NUM[state]))


def message_form_errors(request, form):
    for field, errors in form.errors.items():
        for error in errors:
            readable_field = field.replace('_', ' ').capitalize()
            msg = '{} error: {}'.format(readable_field, error)
            messages.error(request, msg)
