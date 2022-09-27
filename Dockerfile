FROM python:3.10-bullseye

ENV PATH="/env/bin:${PATH}"
WORKDIR /app
COPY requirements.txt /app/
RUN python -m venv /env && \
    pip install -r requirements.txt
COPY . /app/
RUN python manage.py collectstatic
USER nobody
EXPOSE 8000
CMD ["gunicorn", "xteams.wsgi"]
