#!/bin/bash

python3 $PACKAGE_DIR/app.py --port $PORT --host $HOST --debug $dubug >>/app/app.log 2>&1

exec "${@}"
