#!/bin/bash
set -e

SERVICE=website-react-pf-backend
USAGE='usage: deploy.sh <stage>'
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [ $# -lt 1 ]; then
    echo "$USAGE"
    echo '(You forgot to put a stage!)'
    exit 1
fi

echo "Deploying $SERVICE to ${1}!"

poetry install
cd ../../infrastructure/cloudformation
rm -rf cdk.out
poetry install
cdk deploy $1/WebsitePfStack -c stage_name=$1
cd ../../backend/website-pf
