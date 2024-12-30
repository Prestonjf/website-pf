#!/bin/bash
set -e

cd serverless/website-pf
poetry run pytest
cd ../..

cd webapp/website-pf
npm run test
cd ../..
