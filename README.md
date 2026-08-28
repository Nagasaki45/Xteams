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

Development uses a repository-local SQLite database by default; PostgreSQL and Docker are not required. Install Python 3.10 with [uv](https://docs.astral.sh/uv/), then create a project-local environment and install its dependencies:

```bash
uv python install 3.10
uv sync --python 3.10 --extra dev
uv run python manage.py migrate
uv run python manage.py createsuperuser  # optionally
```

You are ready to go! Run:

```bash
uv run python manage.py runserver
```

The development data is stored in `db.sqlite3`, which is ignored by Git. To use PostgreSQL in a deployment, install the optional driver with `uv sync --extra postgres`, then set `DATABASE_URL` to its connection URL; it overrides the SQLite default.

## Tests

The browser-based functional suite is in `functional_tests/`. Run it headlessly with:

```bash
HEADLESS=1 uv run python manage.py test functional_tests
```

It requires Firefox. Omit `HEADLESS=1` to watch the browser run.
