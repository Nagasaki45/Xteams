FROM python:3.10-bullseye

WORKDIR /app
COPY requirements.txt /app/
RUN python -m venv /env && \
    /env/bin/pip install -r requirements.txt
COPY . /app/
RUN /env/bin/python manage.py collectstatic
USER nobody
EXPOSE 8000
CMD ["/env/bin/gunicorn", "xteams.wsgi"]
