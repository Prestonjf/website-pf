#!/bin/bash
set -e

SERVICE=website-pf
USAGE='usage: deploy.sh <stage>'
CONFIG_FILE="../../sonar-project.properties"
VERSION=$(sed -n 's/^sonar.projectVersion=//p' $CONFIG_FILE)

if [ $# -lt 1 ]; then
    echo "$USAGE"
    echo '(You forgot to put a stage!)'
    exit 1
fi

echo "Deploying $SERVICE-webapp to ${1}!"

# build webapp .env file
python3 ../../scripts/create-webapp-config.py $1

# build webapp
export NODE_OPTIONS=--openssl-legacy-provider
npm run-script build

# Remove old webapp content
aws s3 rm s3://website-pf-$1/ --recursive --exclude "posts/*" --exclude "upload/*" --exclude "homepage.jpg" --exclude "featured.yml"  --exclude "robots.txt" --exclude "sitemap.xml" --exclude "rss.xml"
aws s3 cp build/ s3://website-pf-$1/site/$VERSION/ --exclude "posts/*" --exclude "homepage.jpg" --exclude "featured.yml" --exclude "robots.txt" --exclude "sitemap.xml" --exclude "rss.xml" --recursive --cache-control max-age=31536000,s-maxage=2592000

# Upload new webapp content
aws s3 cp build/robots.txt s3://website-pf-$1/ --cache-control max-age=86400,s-maxage=86400
aws s3 cp build/rss.xml s3://website-pf-$1/ --cache-control max-age=86400,s-maxage=86400
aws s3 cp build/featured.yml s3://website-pf-$1/ --cache-control max-age=0,s-maxage=0
aws s3 cp build/sitemap.xml s3://website-pf-$1/ --cache-control max-age=86400,s-maxage=86400
aws s3 cp build/homepage.jpg s3://website-pf-$1/ --cache-control max-age=86400,s-maxage=86400
