import base64
import json

from flask import request
from website_pf_shared.utils import utils as shared_utils

logger = shared_utils.setup_logging()


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
