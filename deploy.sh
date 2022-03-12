#!/bin/bash

if [[ $# -eq 0 ]]; then
    echo "You need to supply a stage to deploy. usage: ./deploy.sh prod"
    exit 1
fi
echo "Deploying website-pf to $1"

build=true
deploy=true
uploadstatic=false
webapponly=false
backendonly=false

CONFIG_FILE="sonar-project.properties"
VERSION=$(sed -n 's/^sonar.projectVersion=//p' $CONFIG_FILE)

for var in "$@"
do
    if [ $var == "nobuild" ]; then
        build=false
    fi
    if [ $var == "nodeploy" ]; then
        deploy=false
    fi
    if [ $var == "static" ]; then
        uploadstatic=true
    fi
    if [ $var == "webapponly" ]; then
        webapponly=true
    fi
    if [ $var == "backendonly" ]; then
        backendonly=true
    fi
done


# install npm/serverless plugins
# serverless deploy
if [[ "$build" = true && "$webapponly" = false ]]; then
    npm install
    serverless deploy -s $1
fi


# build webapp .env file
# build webapp
if [[ "$deploy" = true && "$backendonly" = false ]]; then
    python3 scripts/create-webapp-config.py $1
    npm run-script build --prefix s3-webapp
fi


# Remove old webapp content
# Upload new webapp content
if [[ "$deploy" = true && "$backendonly" = false ]]; then
    aws s3 rm s3://website-pf-$1/ --recursive --exclude "posts/*" --exclude "upload/*" --exclude "featured.yml"  --exclude "robots.txt" --exclude "sitemap.xml" --exclude "rss.xml"
    aws s3 cp s3-webapp/build/ s3://website-pf-$1/site/$VERSION/ --exclude "posts/*" --exclude "featured.yml" --exclude "robots.txt" --exclude "sitemap.xml" --exclude "rss.xml" --recursive --cache-control max-age=31536000,s-maxage=2592000
fi


if [ "$uploadstatic" = true ]; then
    #'aws s3 cp s3-webapp/build/robots.txt s3://website-pf-${self:provider.stage}/posts/ --cache-control max-age=31536000,s-maxage=2592000;
    #aws s3 cp s3-webapp/build/robots.txt s3://website-pf-${self:provider.stage}/upload/ --cache-control max-age=31536000,s-maxage=2592000'
    aws s3 cp s3-webapp/build/robots.txt s3://website-pf-${self:provider.stage}/ --cache-control max-age=86400,s-maxage=86400
    aws s3 cp s3-webapp/build/rss.xml s3://website-pf-${self:provider.stage}/ --cache-control max-age=86400,s-maxage=86400
    aws s3 cp s3-webapp/build/featured.yml s3://website-pf-${self:provider.stage}/ --cache-control max-age=0,s-maxage=0
    aws s3 cp s3-webapp/build/sitemap.xml s3://website-pf-${self:provider.stage}/ --cache-control max-age=86400,s-maxage=86400
fi