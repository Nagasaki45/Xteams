FROM ghcr.io/astral-sh/uv:0.9.21 AS uv

FROM python:3.10-bullseye

COPY --from=uv /uv /uvx /bin/

ENV PATH="/app/.venv/bin:${PATH}" \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

# Install the locked production dependencies before copying application code so
# this layer is cached unless the dependency metadata changes.
COPY pyproject.toml uv.lock README.md /app/
RUN uv sync --frozen --no-dev --extra postgres

COPY . /app/
RUN python manage.py collectstatic

USER nobody
EXPOSE 8000
CMD ["gunicorn", "xteams.wsgi"]
