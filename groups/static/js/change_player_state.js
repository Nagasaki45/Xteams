// ajax calls to move players between 'on_the_court', 'on_the_bench' and 'gone_home'
// dynamically change the counter according to the number of players on the court and on the bench

new Vue({
  el: '#app',
  data: {
    lists: [
      {
        id: 'on_the_court',
        name: 'On the court',
        color: 'green',
        players: _.filter(players, function(o) { return o.state === 'on_the_court'; }),
        buttons: [
          { class: 'btn-danger', newState: 'gone_home', text: 'Gone home' },
          { class: 'btn-warning', newState: 'on_the_bench', text: 'Move to bench' }
        ]
      },
      {
        id: 'on_the_bench',
        name: 'On the bench',
        color: 'orange',
        players: _.filter(players, function(o) { return o.state === 'on_the_bench'; }),
        buttons: [
          { class: 'btn-danger', newState: 'gone_home', text: 'Gone home' },
          { class: 'btn-success', newState: 'on_the_court', text: 'Move to court' }
        ]
      },
      {
        id: 'gone_home',
        name: 'Gone home',
        color: 'red',
        players: _.filter(players, function(o) { return o.state === 'gone_home'; }),
        buttons: [
          { class: 'btn-warning', newState: 'on_the_bench', text: 'Move to bench' },
          { class: 'btn-success', newState: 'on_the_court', text: 'Move to court' }
        ]
      }
    ]
  },
  filters: {
    length: function(array) {
      return array.length;
    }
  },
  transitions: {
    slide: {
      css: false,
      enter: function(el, done) { $(el).hide().slideDown(200, done); },
      leave: function(el, done) { $(el).slideUp(200, done); }
    }
  },
  methods: {
    moveTo: function (player, oldState, newState) {
      var oldList = _.find(this.lists, { id: oldState }),
      newList = _.find(this.lists, { id: newState }),
      indexInOld = oldList.players.indexOf(player);
      oldList.players.splice(indexInOld, 1)
      newList.players.push(player);

      $.ajax({
        url: '/change-state/',
        data: {player_pk: player.pk,
          new_state: newState,
          csrfmiddlewaretoken: window.CSRF_TOKEN},
          type: 'POST'
        });
      }
    }
  })
