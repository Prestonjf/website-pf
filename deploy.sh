#!/bin/bash

# build
sls webappbuild -s $1

# deploy
serverless deploy --nos3sync -s $1
sls s3Clear -s $1
sls s3UploadApp -s $1