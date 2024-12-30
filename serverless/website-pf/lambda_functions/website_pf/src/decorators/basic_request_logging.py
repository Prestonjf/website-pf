from flask import request
from functools import wraps
import logging
from lambda_functions.website_pf.src.utils import utils

logger = logging.getLogger()
utils.setup_logging(logger)


def basic_request_logging(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # get Authrorization Header
        client_id = utils.get_authorization_client_id()
        # get IAM role
        iam_role = utils.get_iam_role()
        logger.info(f'{request.method} {request.path} IAM: {iam_role} ClientId: {client_id}')
        logger.debug(f'Website-pf request body/query params: {request.data}\n{request.args}')
        response = f(*args, **kwargs)
        if response.status_code > 299:
            logger.info(f'Response data: {response.data}')
        else:
            logger.debug(f'Response data: {response.data}')
        logger.info(f'Response status: {response.status}')
        return response
    return decorated_function
