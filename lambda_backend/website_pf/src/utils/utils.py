import boto3
from flask import request
import jsonpickle
from urllib.parse import urlparse
import json
import base64
import logging
from pythonjsonlogger import jsonlogger
from lambda_backend.website_pf.src import config

logger = logging.getLogger()


def serialize_reponse(data):
    return jsonpickle.encode(data, unpicklable=False)


def get_s3_public_url(host_name, s3_path):
    u = urlparse(s3_path)
    return host_name + u.path


def get_s3_object(s3_path):
    try:
        s3 = boto3.resource('s3')
        u = urlparse(s3_path)
        logger.debug('Getting file from s3: {} {}'.format(u.netloc, u.path))
        obj = s3.Object(u.netloc, u.path[1:])
        return obj.get()['Body'].read().decode('utf-8')
    except Exception:
        logger.error('Error retreiving file from s3', exc_info=True)
    return ''


def get_authorization_client_id():
    auth_token = get_authorization_token()
    if auth_token:
        return auth_token['client_id']
    else:
        return ''


def get_authorization_token():
    try:
        req_headers = request.headers
        if 'Authorization' in req_headers:
            authorization = req_headers['Authorization']
            if authorization and authorization.strip().startswith('Bearer'):
                authorization = authorization.replace('Bearer', '', 1)
            authorization_split = authorization.split(".")
            if len(authorization_split) > 1:
                token_claims = authorization_split[1]
                decoded_token = base64.b64decode(token_claims + '==').decode('utf-8')
                return json.loads(decoded_token)
    except Exception:
        logger.error("ERROR: Could not retrieve JWT token", exc_info=True)
    return ''


def get_iam_role():
    return ''


def setup_logging(logger_conf):
    for h in logger_conf.handlers:
        logger_conf.removeHandler(h)
    logHandler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter((
        "%(levelname)s %(message)s %(funcName)s %(asctime)s %(exc_info)s %(name)s %(pathname)s %(args)s"
    ))
    logHandler.setFormatter(formatter)
    logger_conf.addHandler(logHandler)
    logger_conf.setLevel(config.LOG_LEVEL)
    logging.getLogger('boto3').setLevel(logging.ERROR)
    logging.getLogger('botocore').setLevel(logging.ERROR)
    logging.getLogger('aws_xray_sdk').setLevel(logging.ERROR)
    logging.getLogger('urllib3').setLevel(logging.ERROR)
    logging.getLogger('requests').setLevel(logging.ERROR)
    logging.getLogger('mysql.connector').setLevel(logging.ERROR)


setup_logging(logger)
