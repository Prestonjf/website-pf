#!/bin/bash

export FLASK_APP=serverless/websit-pf/lambda_functions/website_pf/app.py
export FLASK_ENV=development

trap 'kill %1; kill %2' SIGINT
flask run & npm start --prefix webapp/website-pf
