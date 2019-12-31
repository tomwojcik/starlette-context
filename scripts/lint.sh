#!/bin/sh -e

export PREFIX=""
if [ -d 'venv' ] ; then
    export PREFIX="venv/bin/"
fi

set -x

${PREFIX}mypy  ../starlette_context --ignore-missing-imports --disallow-untyped-defs
${PREFIX}autoflake --in-place --recursive  ../starlette_context ../tests ../setup.py
${PREFIX}black  ../starlette_context ../tests ../setup.py
${PREFIX}isort --multi-line=3 --trailing-comma --force-grid-wrap=0 --combine-as --line-width 88 --recursive --apply ../starlette_context ../tests --skip __init__.py
