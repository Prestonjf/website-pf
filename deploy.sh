#!/bin/bash

# serverless deploy
serverless deploy -s $1

# build webapp .env file
python3 scripts/create-webapp-config.py $1

# build
sls webappbuild -s $1


sls s3RemoveApp -s $1
sls s3UploadApp -s $1
# sls s3UploadDynamicFiles -s $1
