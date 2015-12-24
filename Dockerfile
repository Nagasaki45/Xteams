FROM python:3.5.1
RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN pip install -r requirements.txt
ENV DJANGO_SETTINGS_MODULE xteams.settings.prod

# Create a volume for static files, shared with Nginx
RUN mkdir /staticfiles
RUN python manage.py collectstatic --noinput --clear
VOLUME /staticfiles

EXPOSE 8000
