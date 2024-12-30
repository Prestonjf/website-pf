# Config
import os

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
WEBSITE_URL = os.environ.get('WEBSITE_URL', 'http://localhost:3001/site/0.7.0')
DATABASE_URL = os.environ.get('DATABASE_URL', 'localhost')
DATABASE_SCHEMA = os.environ.get('DATABASE_SCHEMA', 'website_pf')
DATABASE_USERNAME = os.environ.get('DATABASE_USERNAME', '')
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD', '')
S3_WEBSITE_PF_BUCKET = os.environ.get('S3_WEBSITE_PF_BUCKET', 'website-pf-test')

MODE = 'PROD'
REGION = 'us-east-1'

if 'ENVIRONMENT' not in os.environ:
    MODE = 'TEST'
