#!/bin/sh


echo "Waiting for postgres..."

while ! nc -z "$DB_HOST" "$DB_PORT"; do
  sleep 1
done

echo "PostgreSQL started"


# initialize db
export FLASK_APP=fiar
flask db:init
flask db:fill

gunicorn --worker-class eventlet -w 1 'fiar:app' -b 0.0.0.0:8000
