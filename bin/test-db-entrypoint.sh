#!/bin/bash

# Wait for Postgres to start up
until pg_isready -h db -p 5432
do
  echo 'Waiting for database to start up...'
  sleep 1
done

# Execute your commands here
psql -h localhost -p 5433 -U scrapegod -c 'DROP DATABASE IF EXISTS scrapegod_test;'
psql -h localhost -p 5433 -U postgres -c 'CREATE DATABASE scrapegod_test;'
psql -h localhost -p 5433 -U scrapegod -d scrapegod < /test_db_insert_dump.sql
alembic upgrade head || alembic merge heads && alembic upgrade head

# Run the original entrypoint script to start the Postgres service
/usr/local/bin/docker-entrypoint.sh postgres