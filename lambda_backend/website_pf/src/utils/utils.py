import boto3
from flask import request
import jsonpickle
from urllib.parse import urlparse
import jwt
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
    try:
        req_headers = request.headers
        if 'Authorization' in req_headers:
            authorization = req_headers['Authorization']
            if len(authorization) > 7:
                token = authorization[7:]
                token_decoded = jwt.decode(token, verify=False)
                requestor_id = token_decoded['client_id']
                return requestor_id
    except Exception:
        logger.error("ERROR: Could not retrieve requestor id from JWT token")
    return ''


def get_iam_role():
    try:
        return request.environ.get('context', None).invoked_function_arn
    except Exception:
        logger.error("ERROR: Could not retrieve IAM role from context")
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


setup_logging(logger)
