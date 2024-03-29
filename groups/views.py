from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.views.generic.edit import CreateView, DeleteView, FormMixin
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy

from braces.views import (JSONResponseMixin, AjaxResponseMixin,
                          UserPassesTestMixin, LoginRequiredMixin)
from extra_views import UpdateWithInlinesView

from .models import Group, Player
from .forms import GameForm, PlayerInlineFormSetFactory
from . import utils
from . import grouper


def group_list(request):
    groups = Group.objects.all()
    if request.user.is_authenticated:
        context = {
            'user_groups': groups.filter(managers=request.user),
            'rest_groups': groups.exclude(managers=request.user),
        }
    else:
        context = {'rest_groups': groups}
    return render(request, 'groups/list.html', context)


class GroupCreate(LoginRequiredMixin, CreateView):
    model = Group
    fields = ['name']

    def form_valid(self, form):
        result = super().form_valid(form)
        form.instance.managers.add(self.request.user)
        return result


class GroupDetail(FormMixin, DetailView):
    model = Group
    form_class = GameForm


def team_up(request, pk):
    group = get_object_or_404(Group, pk=pk)
    players = utils.get_group_players(group, 'on_the_court')
    form = GameForm(request.GET, num_of_players=len(players))
    if not form.is_valid():
        utils.message_form_errors(request, form)
        return redirect('groups:detail', pk=group.pk)
    number_of_teams = form.cleaned_data['number_of_teams']
    teams = grouper.create(num_of_groups=number_of_teams, elements=players,
                           key=lambda p: p.score)
    context = {'group': group, 'teams': teams}
    return render(request, 'groups/team_up.html', context)


class Manage(UserPassesTestMixin, UpdateWithInlinesView):
    model = Group
    fields = ['name']
    inlines = [PlayerInlineFormSetFactory]
    template_name = 'groups/manage.html'

    def test_func(self, user):
        group = get_object_or_404(Group, pk=self.kwargs['pk'])
        return user in group.managers.all()


class Delete(DeleteView):
    model = Group
    success_url = reverse_lazy('groups:list')


class ChangeState(JSONResponseMixin, AjaxResponseMixin, View):
    """Ajax view to change the players state."""
    def post_ajax(self, request):
        player = get_object_or_404(Player, pk=request.POST['player_pk'])
        player.state_name = request.POST['new_state']
        player.save()
        return self.render_json_response({})
