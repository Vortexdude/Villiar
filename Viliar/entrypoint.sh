#!/bin/bash

python3 $PACKAGE_DIR/app.py --port=$PORT --host=$HOST --debug=$DEBUG >>/app/app.log 2>&1

exec "${@}"
