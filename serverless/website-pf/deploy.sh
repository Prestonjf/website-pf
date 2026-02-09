#!/bin/bash
set -e

SERVICE=website-pf
USAGE='usage: deploy.sh <stage>'

if [ $# -lt 1 ]; then
    echo "$USAGE"
    echo '(You forgot to put a stage!)'
    exit 1
fi

echo "Deploying $SERVICE-serverless to ${1}!"

poetry install
npx serverless deploy -s $1
