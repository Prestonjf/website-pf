import jsonpickle
from urllib.parse import urlparse
import boto3
import config
import logging

logger = logging.getLogger(__file__)
logger.setLevel(config.LOG_LEVEL)


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
