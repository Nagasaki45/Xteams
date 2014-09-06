from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.views.generic.edit import CreateView
from django.contrib import messages

from braces.views import (JSONResponseMixin, AjaxResponseMixin,
                          UserPassesTestMixin, LoginRequiredMixin)
from extra_views import InlineFormSetView

from .models import PLAYING_STATES, Team, Player
from .forms import GameForm
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


def team_detail(request, pk):
    team = get_object_or_404(Team, pk=pk)
    # players on the court, on the bench and gone home as dict
    context = {key: team.player_set.filter(state=value)
               for key, value in PLAYING_STATES.items()}
    context['team'] = team
    context['form'] = GameForm()
    return render(request, 'teams/team_detail.html', context)


def groups(request, pk):
    team = get_object_or_404(Team, pk=pk)
    players = list(
        team.player_set.filter(state=PLAYING_STATES['on_the_court'])
    )
    num_of_groups = int(request.GET['num_of_groups'])
    chance = float(request.GET['chance'])
    try:
        groups = grouper.create(num_of_groups=num_of_groups,
                                elements=players,
                                key=lambda p: p.score,
                                chance=chance)
        return render(request, 'teams/groups.html', {'groups': groups})
    except grouper.GrouperError as e:
        messages.error(request, str(e))
        return redirect('teams:detail', pk=team.pk)


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
