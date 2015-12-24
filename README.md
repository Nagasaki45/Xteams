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

Instead of global postgres installation I'm using postgres in a docker container in development. So make sure you have docker and docker-compose available on your dev machine.

First, run the initial requirements and local database setup:

```bash
$ # Using a Python virtualenv is highly recommended
$ virtualenv virtualenv -p python3 --no-site-packages
$ source ./virtualenv/bin/activate
$ pip install -r requirements.txt
$ docker-compose up -d  # to spin postgres
$ python manage.py migrate
```

For the contact page to work you will also need to:

```bash
export ADMIN=yourname
export ADMIN_EMAIL=your@email.com
export EMAIL_HOST_USER=your_email_username
export EMAIL_HOST_PASSWORD=your_email_password
```

Ideally, you can append the following to the bottom of your virtualenv activate script. (found in `virtualenv/bin/activate`).

If you are on gmail the above is just enough, otherwise take a look on the settings file and apply necessary changes.

You are ready to go, run:

```bash
$ python manage.py createsuperuser  # optionally
$ python manage.py runserver
```
