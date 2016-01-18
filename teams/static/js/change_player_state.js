// Xteams! Sport teams management utility
// Copyright (C) 2014  Tom Gurion

// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.

/////////////////////////////////////////////////

// ajax calls to move players between 'on_the_court', 'on_the_bench' and 'gone_home'
// dynamically change the counter according to the number of players on the court and on the bench

new Vue({
  el: '#app',
  data: {
    lists: [
      {
        id: 'on_the_court',
        name: 'On the court',
        players: starting_players.on_the_court,
        buttons: [
          { class: 'btn-danger', newState: 'gone_home', text: 'Gone home' },
          { class: 'btn-warning', newState: 'on_the_bench', text: 'Move to bench' }
        ]
      },
      {
        id: 'on_the_bench',
        name: 'On the bench',
        class: 'list-group-item-warning',
        players: starting_players.on_the_bench,
        buttons: [
          { class: 'btn-danger', newState: 'gone_home', text: 'Gone home' },
          { class: 'btn-success', newState: 'on_the_court', text: 'Move to court' }
        ]
      },
      {
        id: 'gone_home',
        name: 'Gone home',
        class: 'list-group-item-danger',
        players: starting_players.gone_home,
        buttons: [
          { class: 'btn-warning', newState: 'on_the_bench', text: 'Move to bench' },
          { class: 'btn-success', newState: 'on_the_court', text: 'Move to court' }
        ]
      }
    ]
  },
  computed: {
    on_the_court_counter: function () {
      return this.lists[0].players.length;
    },
    arrived_counter: function() {
      return this.on_the_court_counter + this.lists[1].players.length;
    }
  },
  methods: {
    moveTo: function (player, oldState, newState) {
      var that = this;
      // Remove the player from the current list
      $.each(that.lists, function(i) {
        if (that.lists[i].id === oldState) {
          that.lists[i].players = that.lists[i].players.filter(function (p) {
            return p.pk !== player.pk;
          });
        }
        // Add the player to the new list
        if (that.lists[i].id === newState) {
          that.lists[i].players.push(player);
        }
      });

      $.ajax({
        url: '/change-state/',
        data: {player_pk: player.pk, new_state: newState},
        type: 'POST',
        beforeSend: function(request) {
            request.setRequestHeader('X-CSRFToken', $.cookie('csrftoken'));
        }
      });
    }
  }
})
