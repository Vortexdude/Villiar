#!/bin/bash

cd $PACKAGE_DIR
alembic upgrade head >> /app/db.log 2>&1

gunicorn 'app:app' -w ${WORKER_COUNT} -b ${HOST}:${PORT} >>/app/app.log 2>&1

exec "${@}"
