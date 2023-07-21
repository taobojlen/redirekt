FROM python:3

ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION=1.3.1
ENV POETRY_HOME=/opt/poetry

WORKDIR /app

ARG APK_MIRROR=https://dl-cdn.alpinelinux.org/alpine/

RUN apt-get update
RUN apt-get install nodejs npm -y
COPY package.json package-lock.json ./
COPY frontend/ frontend/
COPY tsconfig.json vite.config.ts ./
RUN npm ci
RUN npm run build

COPY pyproject.toml poetry.lock ./
RUN --mount=type=cache,target=/var/cache/pip python -m venv ${POETRY_HOME} \
    && ${POETRY_HOME}/bin/pip install "poetry==$POETRY_VERSION" --cache-dir /var/cache/pip \
    && ${POETRY_HOME}/bin/poetry export -f requirements.txt --output requirements.txt --without dev \
    && pip install -r requirements.txt --compile --cache-dir /var/cache/pip

# Add in Django deps and generate Django's static files
COPY manage.py manage.py
COPY redirekt redirekt/
COPY links links/
COPY admin admin/
COPY docker-entrypoint.sh docker-entrypoint.sh

RUN python manage.py collectstatic --noinput

EXPOSE 8000
ENV DJANGO_SETTINGS_MODULE=redirekt.settings.production
CMD ["bash", "docker-entrypoint.sh"]
