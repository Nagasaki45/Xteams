Xteams!
=======

You want to create teams, but:

- How can one create teams when Dana doesn't want to play with Haim, who must play with Jacob but not with Yossi... You've got the idea.

- No one will ever want to help in creating teams as he may end up insulting a not-so-good player by choosing him last.

- Maybe you have too many players around for one game, but just enough for a tournament of 4 teams.

Xteams aim to solve these issues with one goal in mind:

_Create teams automatically based on discrete scores of the players_

Using Xteams, group managers can give scores to players in the management panel. Players of the group can't access this panel but can see the list of players, mark which of them arrived to the game and create teams easily.

## Development

First, run the initial requirements and local database setup:

```bash
$ virtualenv xteams  # Using a Python virtualenv is highly recommended
$ pip install -r requirements.txt
$ python manage.py syncdb
```

Make sure you use Python 3.4 and you are ready to go :-)
