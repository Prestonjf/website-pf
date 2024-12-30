#!/bin/bash
set -e

if [[ $# -eq 0 ]]; then
    echo "You need to supply a stage to deploy. usage: ./deploy.sh prod"
    exit 1
fi
echo "Deploying website-pf to $1"

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

# Install deployment tools 
python3 -m venv .website-pf-venv
source .website-pf-venv/bin/activate
pip3 install -r scripts/requirements.txt 
npm install

# serverless deploy
if [[ "$skipServerless" = false ]]; then
    cd serverless/website-pf
    npx serverless deploy -s $1
    cd ../..
fi

# build webapp .env file
# build webapp
# Remove old webapp content
# Upload new webapp content
if [[ "$skipWebapp" = false ]]; then
    python3 scripts/create-webapp-config.py $1
    cd webapp/website-pf
    npm run-script build

    aws s3 rm s3://website-pf-$1/ --recursive --exclude "posts/*" --exclude "upload/*" --exclude "homepage.jpg" --exclude "featured.yml"  --exclude "robots.txt" --exclude "sitemap.xml" --exclude "rss.xml"
    aws s3 cp build/ s3://website-pf-$1/site/$VERSION/ --exclude "posts/*" --exclude "homepage.jpg" --exclude "featured.yml" --exclude "robots.txt" --exclude "sitemap.xml" --exclude "rss.xml" --recursive --cache-control max-age=31536000,s-maxage=2592000

    aws s3 cp build/robots.txt s3://website-pf-$1/ --cache-control max-age=86400,s-maxage=86400
    aws s3 cp build/rss.xml s3://website-pf-$1/ --cache-control max-age=86400,s-maxage=86400
    aws s3 cp build/featured.yml s3://website-pf-$1/ --cache-control max-age=0,s-maxage=0
    aws s3 cp build/sitemap.xml s3://website-pf-$1/ --cache-control max-age=86400,s-maxage=86400
    aws s3 cp build/homepage.jpg s3://website-pf-$1/ --cache-control max-age=86400,s-maxage=86400
    cd ../..
fi

# Cleanup deployment
deactivate
# log deployment completion and seconds