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
$ # virtualenv is highly recommended
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements/run.txt
$ docker-compose up -d  # to spin postgres
$ python manage.py migrate
```

You are ready to go, run:

```bash
$ python manage.py createsuperuser  # optionally
$ python manage.py runserver
```

### Requirements files

There are 3 requirements files:
- For running the app you only need to `pip install requirements/run.txt`
- For running the test you will also have to `pip install requirements/test.txt`
- I'm using one extra requirement file for development, but nothing really depends on it.

### env_file

Secrets are kept in a file in the root directory of the project, named `env_file`. Create one and populate it with:

```
ADMIN=<Your name>
ADMIN_EMAIL=<Your email>
MAILGUN_ACCESS_KEY=<key>
MAILGUN_SERVER_NAME=<domain>
```

docker-compose will use this env_file automatically (notice the format, there are no exports).
Although it's possible to run without it in development, you probably want to export each line. If you use some kind of autoenv the `.env` file will export each line for you. Otherwise you can source the `.env` file manually, or export manually, as you prefer.

## Production / staging

Run the production environment on port 9768 (random number, to allow multiple apps on the same server) with:

```bash
$ docker-compose -f docker-compose-prod.yml up -d
```

It will configure the following docker containers: Nginx http server -> webapp (running with gunicorn) -> postgres db.

The webapp collects static files into a volume shared with the Nginx container for the second to serve static files directly.

You can set the Nginx on the host to route traffic to the Nginx container with:

```
# /etc/nginx/sites-available/xteams.nagasaki45.com

server {
    listen 80;
    server_name xteams.nagasaki45.com;

    location / {
        proxy_set_header Host xteams.nagasaki45.com;
        proxy_pass http://localhost:9768;
    }
}
```

Add a link to `sites-enabled`:

```bash
ln -s /etc/nginx/sites-available/xteams.nagasaki45.com /etc/nginx/sites-enabled/xteams.nagasaki45.com
```

Restart your host Nginx with `service nginx restart`.
