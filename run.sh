#!/bin/bash

export FLASK_APP=lambda_backend/website_pf/app.py
export FLASK_ENV=development

trap 'kill %1; kill %2' SIGINT
flask run & npm start --prefix s3-webapp
