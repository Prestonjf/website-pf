#!/bin/bash

# test
poetry run pytest --cov
poetry run coverage xml


# build
sls webappbuild -s $1

# deploy
serverless deploy -s $1
sls s3RemoveApp -s $1
sls s3UploadApp -s $1
# sls s3UploadDynamicFiles -s $1
