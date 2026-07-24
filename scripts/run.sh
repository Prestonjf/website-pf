#!/bin/bash

export FLASK_APP=../backend/website-pf/src/website_pf_api/app.py
export FLASK_ENV=development

trap 'kill %1; kill %2' SIGINT
flask run & npm start --prefix ../frontend/website-pf
