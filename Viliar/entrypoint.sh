#!/bin/bash

chmod +x ./run.sh

bash $PACKAGE_DIR/script/run.sh >>/root/app.log 2>&1

python3 $PACKAGE_DIR/app.py --port $PORT --host $HOST >>/root/app.log 2>&1

exec "${@}"
