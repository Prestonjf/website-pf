#!/bin/bash
set -e

SERVICE=website-pf
USAGE='usage: deploy.sh <stage>'

if [ $# -lt 1 ]; then
    echo "$USAGE"
    echo '(You forgot to put a stage!)'
    exit 1
fi

skipServerless=false
skipWebapp=false

CONFIG_FILE="sonar-project.properties"
VERSION=$(sed -n 's/^sonar.projectVersion=//p' $CONFIG_FILE)

for var in "$@"
do
    if [ $var == "skipServerless" ]; then
        skipServerless=true
    fi
    if [ $var == "skipWebapp" ]; then
        skipWebapp=true
    fi
done

echo "Deploying $SERVICE $VERSION to ${1} at $(date)!"

# Install deployment tools 
python3 -m venv .website-pf-venv
source .website-pf-venv/bin/activate
pip3 install -r scripts/requirements.txt 
npm install

# serverless deploy
if [[ "$skipServerless" = false ]]; then
    cd serverless/website-pf
    ./deploy.sh $1
    cd ../..
fi

# webapp deploy
if [[ "$skipWebapp" = false ]]; then
    cd webapp/website-pf
    ./deploy.sh $1
    cd ../..
fi

# Cleanup deployment
deactivate
# log deployment completion and seconds

echo "Deployed $SERVICE $VERSION to ${1} at $(date) completed in $SECONDS seconds!"
