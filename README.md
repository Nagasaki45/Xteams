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
$ # I prefer conda environments, but virtualenvs will work similarly
$ # just notice the .env and .out files
$ conda create --name Xteams python=3.5.1
$ source activate Xteams
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

## Staging

Run the staging environment on port 8000 with:

```bash
$ docker-compose -f docker-compose-stage.yml up  # consider using -d flag for running in the background
```

It will configure the following docker containers: Nginx http server -> webapp (running with gunicorn) -> postgres db.

The webapp collects static files into a volume shared with the Nginx container for the second to serve static files directly.

## Production

Staging and production are almost the same. The only difference is that in production Nginx is listening on port 9768 (random number), to let the Nginx on the host route traffic to all of the apps on the host.

Run:

```bash
docker-compose -f docker-compose-stage.yml -f docker-compose-prod.yml up -d
```

Set the host Nginx to route traffic to the Nginx container. Something like this:

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
