#!/bin/sh

PYTHON_VERSION_TARGET=3.7.0

set -e


if which pyenv > /dev/null
then
  echo "Pyenv found"
  pyenv versions | grep -q $PYTHON_VERSION_TARGET || pyenv install $PYTHON_VERSION_TARGET
  pyenv local $PYTHON_VERSION_TARGET
fi

ver=$(python3 -V 2>&1 | sed 's/.* \([0-9]\).\([0-9]\).*/\1\2/')
if [ "$ver" -lt "37" ]; then
    echo "This script requires python 3.7 or greater"
    exit 1
fi

if [ -d venv ]; then rm -r venv; fi
python3 -m venv venv
. ./venv/bin/activate; \
pip install --upgrade pip; \
pip install wheel; \
pip install -r requirements-dev.txt
