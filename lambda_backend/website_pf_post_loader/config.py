# Config
import os
from ruamel.yaml import YAML

if 'ENVIRONMENT' not in os.environ:
    with open(os.getcwd() + '/config/local.yml') as f:
        yaml = YAML(typ='safe')
        data = yaml.load(f)
        LOG_LEVEL = data['logLevel']
        DATABASE_URL = data['databaseUrl']
        DATABASE_SCHEMA = data['databaseSchema']
        DATABASE_USERNAME = data['databaseUsername']
        DATABASE_PASSWORD = data['databasePassword']
        WEBSITE_URL = data['websiteUrl']
        MODE = 'TEST'
else:
    LOG_LEVEL = os.environ['LOG_LEVEL']
    WEBSITE_URL = os.environ['WEBSITE_URL']
    DATABASE_URL = os.environ['DATABASE_URL']
    DATABASE_SCHEMA = os.environ['DATABASE_SCHEMA']
    DATABASE_USERNAME = os.environ['DATABASE_USERNAME']
    DATABASE_PASSWORD = os.environ['DATABASE_PASSWORD']
    MODE = 'PROD'
