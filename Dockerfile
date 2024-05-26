FROM python:3.9.2-alpine

WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Pillow and psycopg2 dependencies
RUN apk update \
    && apk add gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && apk add jpeg-dev zlib-dev libjpeg

# Install Python dependencies
COPY requirements.lock /usr/src/app
RUN pip install --upgrade pip
RUN pip install -r requirements.lock
RUN pip install psycopg2-binary==2.8.3
RUN pip install gunicorn==19.9.0

# Copy Python files
COPY ./settings/ /usr/src/app/settings/
COPY ./apps/ /usr/src/app/apps/
COPY ./manage.py /usr/src/app/
