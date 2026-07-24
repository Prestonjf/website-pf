import mysql.connector

from website_pf_api import config
from website_pf_shared.utils import utils as shared_utils

logger = shared_utils.setup_logging()


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
    return shared_utils.serialize_reponse(records)
