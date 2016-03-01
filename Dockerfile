FROM python:3.5.1
RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN pip install -r requirements/run.txt
ENV DJANGO_SETTINGS_MODULE xteams.settings.prod
