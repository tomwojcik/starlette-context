#!/bin/sh -e

export PREFIX=""
if [ -d 'venv' ] ; then
    export PREFIX="venv/bin/"
fi

set -x

${PREFIX}pytest .. --ignore venv --cov=starlette_context/starlette_context --cov-report=term-missing
#${PREFIX}mypy ../starlette_context/starlette_context --ignore-missing-imports --disallow-untyped-defs
