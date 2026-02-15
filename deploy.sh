#!/bin/bash
set -e

SERVICE=website-pf
USAGE='usage: deploy.sh <stage>'

if [ $# -lt 1 ]; then
    echo "$USAGE"
    echo '(You forgot to put a stage!)'
    exit 1
fi

skipCloudformation=false
skipWebapp=false

CONFIG_FILE="sonar-project.properties"
VERSION=$(sed -n 's/^sonar.projectVersion=//p' $CONFIG_FILE)

for var in "$@"
do
    if [ $var == "skipCloudformation" ]; then
        skipCloudformation=true
    fi
    if [ $var == "skipWebapp" ]; then
        skipWebapp=true
    fi
done

echo "Deploying $SERVICE $VERSION to ${1} at $(date)!"

# Install deployment tools 
poetry install

# serverless deploy
if [[ "$skipCloudformation" = false ]]; then
    cd backend/website-pf
    ./deploy.sh $1
    cd ../..
fi

# webapp deploy
if [[ "$skipWebapp" = false ]]; then
    cd frontend/website-pf
    ./deploy.sh $1
    cd ../..
fi

# log deployment completion and seconds
echo "Deployed $SERVICE $VERSION to ${1} at $(date) completed in $SECONDS seconds!"
