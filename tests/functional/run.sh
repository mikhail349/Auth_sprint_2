#!/bin/bash

[[ -z "$DB_HOST" ]] && { echo "Parameter DB_HOST is empty" ; exit 1; }
[[ -z "$DB_PORT" ]] && { echo "Parameter DB_PORT is empty" ; exit 1; }

while ! nc -z $DB_HOST $DB_PORT; do
    sleep 0.1
done

cd tests/functional
flask --app conftest db upgrade --directory ../../src/app/migrations
pytest