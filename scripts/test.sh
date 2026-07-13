#!/bin/bash
set -e

POETRY_CMD="install"
for var in "$@"
do
    if [ $var == "update" ]; then
        POETRY_CMD="update"
    fi
done

cd ../backend/website-pf
poetry $POETRY_CMD
poetry run pytest
cd ../..

cd ../frontend/website-pf
npm run test
cd ../..
