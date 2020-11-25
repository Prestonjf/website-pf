import logging
import mysql.connector
from src.utils import utils
import config

logger = logging.getLogger(__file__)
logger.setLevel(config.LOG_LEVEL)


def database_handler(query, params):
    records = {}
    posts = []
    try:

        cnx = mysql.connector.connect(
            host=config.DATABASE_URL,
            database=config.DATABASE_SCHEMA,
            user=config.DATABASE_USERNAME,
            password=config.DATABASE_PASSWORD)
        cursor = cnx.cursor(prepared=True)

        cursor.execute(query, params)

        for r in cursor:
            posts.append(r)

        logger.debug(posts)
        cursor.close()
        cnx.close()
    except Exception:
        logger.error('Error connecting to database', exc_info=True)
    records['posts'] = posts
    return utils.serialize_reponse(records)
