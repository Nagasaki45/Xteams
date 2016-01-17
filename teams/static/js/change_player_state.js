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

$(document).ready(function() {

    var moveToCourtButton = '<p class="to-court btn btn-xs btn-success pull-right margins">Move to Court</p>',
        moveToBenchButton = '<p class="to-bench btn btn-xs btn-warning pull-right margins">Move to bench</p>',
        moveToHomeButton = '<p class="to-home btn btn-xs btn-danger pull-right margins">Gone home</p>',
        setCounters = function() {
            var on_the_court = $('#on_the_court').children().length - 1,  // -1 for the title
                on_the_bench = $('#on_the_bench').children().length - 1,  // -1 for the title
                arrived = on_the_court + on_the_bench;
            $('#on_the_court_counter').text(on_the_court);
            $('#arrived_counter').text(arrived);
        },
        moveTo = function(playerPk, newState) {
            var element = $('#' + playerPk);
            $.ajax({
                url: '/change-state/',
                data: {player_pk: playerPk, new_state: newState},
                type: 'POST',
                beforeSend: function(request) {
                    request.setRequestHeader('X-CSRFToken', $.cookie('csrftoken'));
                }
            });
            // move it to the new place
            element.appendTo($('#' + newState));
            // remove its buttons
            element.children().remove();
            // remove all unique classes
            element.removeClass('list-group-item-danger');
            element.removeClass('list-group-item-warning');
            // add new buttons and classes
            if (newState == 'on_the_court') {
                $(moveToHomeButton)
                .on('click', function() {
                    moveTo($(this).parent().attr('id'), 'gone_home')
                })
                .appendTo(element);
                $(moveToBenchButton)
                .on('click', function() {
                    moveTo($(this).parent().attr('id'), 'on_the_bench')
                })
                .appendTo(element);
            } else if (newState == 'on_the_bench') {
                element.addClass('list-group-item-warning');
                $(moveToHomeButton)
                .on('click', function() {
                    moveTo($(this).parent().attr('id'), 'gone_home')
                })
                .appendTo(element);
                $(moveToCourtButton)
                .on('click', function() {
                    moveTo($(this).parent().attr('id'), 'on_the_court')
                })
                .appendTo(element);
            } else if (newState == 'gone_home') {
                element.addClass('list-group-item-danger');
                $(moveToBenchButton)
                .on('click', function() {
                    moveTo($(this).parent().attr('id'), 'on_the_bench')
                })
                .appendTo(element);
                $(moveToCourtButton)
                .on('click', function() {
                    moveTo($(this).parent().attr('id'), 'on_the_court')
                })
                .appendTo(element);
            }
            setCounters();
        };

    $('.to-court').on('click', function() {
        moveTo($(this).parent().attr('id'), 'on_the_court')
    });

    $('.to-bench').on('click', function() {
        moveTo($(this).parent().attr('id'), 'on_the_bench')
    });

    $('.to-home').on('click', function() {
        moveTo($(this).parent().attr('id'), 'gone_home')
    });

    setCounters();
});
