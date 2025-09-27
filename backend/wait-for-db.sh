#!/bin/sh
# Wait until MySQL is ready
echo "Waiting for database at $DB_HOST:$DB_PORT..."
while ! mysqladmin ping -h"$DB_HOST" -P"$DB_PORT" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" --silent; do
    echo "Database is unavailable - sleeping"
    sleep 2
done
echo "Database is up - continuing..."
exec "$@"
