Xteams!
=======

[ ![Codeship Status for Nagasaki45/Xteams](https://codeship.com/projects/aa1e00d0-bb05-0133-640e-6efa14f009c2/status?branch=master)](https://codeship.com/projects/135768)
[![Coverage Status](https://coveralls.io/repos/github/Nagasaki45/Xteams/badge.svg?branch=master)](https://coveralls.io/github/Nagasaki45/Xteams?branch=master)

You want to create teams, but:

- How can one create teams when Dana doesn't want to play with Haim, who must play with Jacob but not with Yossi... You've got the idea.

- No one will ever want to help in creating teams as he may end up insulting a not-so-good player by choosing him last.

- Maybe you have too many players around for one game, but just enough for a tournament of 4 teams.

Xteams aim to solve these issues with one goal in mind:

_Create teams automatically based on discrete scores of the players_

Using Xteams, group managers can give scores to players in the management panel. Players of the group can't access this panel but can see the list of players, mark which of them arrived to the game and create teams easily.

## Development

Install postgres.

Now, run install dependencies and setup the database:

```bash
$ python -m venv env  # virtualenv is highly recommended
$ source env/bin/activate
$ pip install -r requirements.txt  # or use pip-tools
$ python manage.py migrate
$ python manage.py createsuperuser  # optionally
```

You are ready to go! Run:

```bash
$ python manage.py runserver
```
