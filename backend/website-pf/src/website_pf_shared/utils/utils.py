import logging
import sys
from logging import Logger, getLogger
from os import getenv
from urllib.parse import urlparse

import boto3
import jsonpickle
from pythonjsonlogger.json import JsonFormatter

logger = None


def serialize_reponse(data):
    return jsonpickle.encode(data, unpicklable=False)


def get_s3_public_url(host_name, s3_path):
    u = urlparse(s3_path)
    return host_name + u.path


def get_s3_object(s3_path):
    try:
        s3 = boto3.resource('s3')
        u = urlparse(s3_path)
        logger.debug('Getting file from s3: %s %s', u.netloc, u.path)
        obj = s3.Object(u.netloc, u.path[1:])
        return obj.get()['Body'].read().decode('utf-8')
    except Exception:
        logger.error('Error retreiving file from s3', exc_info=True)
    return ''


def setup_logging(name: str = "website_pf", level: str = None) -> Logger:
    logger_conf = getLogger(name)
    logger_conf.propagate = False
    log_level = level if level else getenv("LOG_LEVEL", "INFO")

    for handler in list(logger_conf.handlers):
        logger_conf.removeHandler(handler)

    log_handler = logging.StreamHandler(sys.stdout)
    formatter = JsonFormatter((
        "%(levelname)s %(message)s %(funcName)s %(asctime)s %(exc_info)s %(name)s %(pathname)s %(args)s"
    ))
    log_handler.setFormatter(formatter)
    logger_conf.addHandler(log_handler)
    logger_conf.setLevel(log_level)

    logging.getLogger('boto3').setLevel(logging.ERROR)
    logging.getLogger('botocore').setLevel(logging.ERROR)
    logging.getLogger('aws_xray_sdk').setLevel(logging.ERROR)
    logging.getLogger('urllib3').setLevel(logging.ERROR)
    logging.getLogger('requests').setLevel(logging.ERROR)
    logging.getLogger('mysql.connector').setLevel(logging.ERROR)

    return logger_conf


logger = setup_logging()
