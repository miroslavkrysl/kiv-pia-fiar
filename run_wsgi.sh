#!/bin/sh


if [ "$DB_DRIVER" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z "$DB_HOST" "$DB_PORT"; do
      sleep 1
    done

    echo "PostgreSQL started"
fi


# initialize db
export FLASK_APP=fiar
flask init-db

gunicorn --worker-class eventlet -w 1 'fiar:app'
