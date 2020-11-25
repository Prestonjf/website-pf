import logging
from flask import request
from functools import wraps
from src.utils import utils
import config

logger = logging.getLogger('app.decorators.basic_request_logging')
logger.setLevel(logging._nameToLevel[config.LOG_LEVEL])


def basic_request_logging(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # get Authrorization Header
        client_id = utils.get_authorization_client_id()
        # get IAM role
        iam_role = utils.get_iam_role()
        logger.info(f'{request.method} {request.path} \n IAM: {iam_role} ClientId: {client_id}')
        logger.debug(f'Website-pf request body/query params:\n{request.data}\n{request.args}')
        response = f(*args, **kwargs)
        if response.status_code > 299:
            logger.info(f'Response data: {response.data}')
        else:
            logger.debug(f'Response data: {response.data}')
        logger.info(f'Response status: {response.status}')
        return response
    return decorated_function
