#!/bin/bash

cd $PACKAGE_DIR
alembic upgrade head >> /app/db.log 2>&1
python3 app.py --port=$PORT --host=$HOST --debug=$DEBUG >>/app/app.log 2>&1

exec "${@}"
