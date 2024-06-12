#!/usr/bin/env bash

set -ex

create_schema_hash="c229dfbbae52"
data_injection_has="514833f6866d"

PACKAGE_NAME="Viliar"
CUR_DIR=$(cd "$(dirname "$0")" && pwd)
PACKAGE_DIR="${CUR_DIR}/../"

##### SETUP THE PYTHON VARS #####
SYSTEM_PYTHON=python3
VENV="${PACKAGE_DIR}${PACKAGE_NAME}/.venv"
VENV_PYTHON="${VENV}/bin/python3"
VENV_PIP="${VENV}/bin/pip3"

cd $PACKAGE_DIR || exit
$SYSTEM_PYTHON -m venv ${PACKAGE_NAME}/.venv
. "${VENV}/bin/activate"

$VENV_PYTHON -m pip install --upgrade pip
$VENV_PIP install --upgrade -q -r "$PACKAGE_DIR"requirements.txt


##### run alembic #####
cd ${PACKAGE_NAME}
alembic upgrade "$create_schema_hash"
alembic upgrade "$data_injection_has"




#pip3 install -r "$PACKAGE_DIR"requirements.txt

