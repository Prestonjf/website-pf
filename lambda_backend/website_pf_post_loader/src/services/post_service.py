# Post Services
from src.repositories import mysql_repository
import config
import logging

logger = logging.getLogger('app.services.post_service')
logger.setLevel(config.LOG_LEVEL)


def get_recent_posts():
    try:
        return ''
    except Exception:
        logger.error('Error retreiving file from s3', exc_info=True)
        return ''
