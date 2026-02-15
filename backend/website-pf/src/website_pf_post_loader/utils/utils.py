import boto3
import jsonpickle
from urllib.parse import urlparse
import logging
from pythonjsonlogger.json import JsonFormatter
from website_pf_post_loader import config

logger = logging.getLogger(__file__)


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


def setup_logging(logger):
    for h in logger.handlers:
        logger.removeHandler(h)
    logHandler = logging.StreamHandler()
    formatter = JsonFormatter((
        "%(levelname)s %(message)s %(funcName)s %(asctime)s %(exc_info)s %(name)s %(pathname)s %(args)s %(levelno)s"
    ))
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)
    logger.setLevel(config.LOG_LEVEL)
    logging.getLogger('boto3').setLevel(logging.ERROR)
    logging.getLogger('botocore').setLevel(logging.ERROR)
    logging.getLogger('aws_xray_sdk').setLevel(logging.ERROR)
    logging.getLogger('urllib3').setLevel(logging.ERROR)
    logging.getLogger('requests').setLevel(logging.ERROR)
    logging.getLogger('mysql.connector').setLevel(logging.ERROR)


setup_logging(logger)
