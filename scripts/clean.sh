#!/bin/sh -e

if [ -d 'dist' ] ; then
    rm -r dist
fi
if [ -d 'site' ] ; then
    rm -r site
fi
if [ -d 'htmlcov' ] ; then
    rm -r htmlcov
fi
if [ -d 'starlette_context.egg-info' ] ; then
    rm -r starlette_context.egg-info
fi

find . -type d -name ".*" -empty -delete
