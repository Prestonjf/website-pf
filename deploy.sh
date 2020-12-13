#!/bin/bash

# build
sls webappbuild -s $1

# deploy
serverless deploy -s $1
sls s3RemoveApp -s $1
sls s3UploadApp -s $1
