#!/bin/bash

docker exec `docker ps -a -q | head -n 1` python manage.py migrate
