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

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.views.generic.edit import CreateView, FormMixin
from django.views.generic.detail import DetailView
from django.http import HttpResponseBadRequest

from braces.views import (JSONResponseMixin, AjaxResponseMixin,
                          UserPassesTestMixin, LoginRequiredMixin)
from extra_views import InlineFormSetView

from .models import PLAYING_STATES, Team, Player
from .forms import GameForm
from . import utils
from . import grouper


def team_list(request):
    teams = Team.objects.all()
    if request.user.is_authenticated():
        context = {
            'user_teams': teams.filter(managers=request.user),
            'rest_teams': teams.exclude(managers=request.user),
        }
    else:
        context = {'rest_teams': teams}
    return render(request, 'teams/team_list.html', context)


class TeamCreate(LoginRequiredMixin, CreateView):
    model = Team
    fields = ['name']

    def form_valid(self, form):
        result = super().form_valid(form)
        form.instance.managers.add(self.request.user)
        return result


class GroupDetail(FormMixin, DetailView):
    model = Team
    form_class = GameForm


def groups(request, pk):
    team = get_object_or_404(Team, pk=pk)
    players = utils.get_group_players(team, 'on_the_court')
    form = GameForm(request.GET, num_of_players=len(players))
    if not form.is_valid():
        utils.message_form_errors(request, form)
        return redirect('teams:detail', pk=team.pk)
    number_of_teams = form.cleaned_data['number_of_teams']
    groups = grouper.create(num_of_groups=number_of_teams, elements=players,
                            key=lambda p: p.score)
    context = {'team': team, 'groups': groups}
    return render(request, 'teams/groups.html', context)


class Manage(UserPassesTestMixin, InlineFormSetView):
    model = Team
    inline_model = Player
    fields = ['name', 'score']
    extra = 5
    template_name = 'teams/manage.html'

    def test_func(self, user):
        team = get_object_or_404(Team, pk=self.kwargs['pk'])
        return user in team.managers.all()


class ChangeState(JSONResponseMixin, AjaxResponseMixin, View):

    '''
    Ajax view to change the players state.
    POST data includes player_pk and new_state valeus.
    '''

    def post_ajax(self, request):
        player = get_object_or_404(Player, pk=request.POST['player_pk'])
        player.state = PLAYING_STATES[request.POST['new_state']]
        player.save()
        return self.render_json_response({})
