#!/bin/bash
set -e

SERVICE=website-react-pf-backend
USAGE='usage: deploy.sh <stage>'

if [ $# -lt 1 ]; then
    echo "$USAGE"
    echo '(You forgot to put a stage!)'
    exit 1
fi

echo "Deploying $SERVICE to ${1}!"

poetry install
cd ../../infrastructure/cloudformation
poetry install
cdk deploy $1/WebsitePf -c stage_name=$1
cd ../../bqckend/website-pf
