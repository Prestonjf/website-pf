# MySQL Services.
import logging
import mysql.connector
from lambda_backend.website_pf_post_loader.src import config

logger = logging.getLogger('app.repositories.mysql_repository')
logger.setLevel(config.LOG_LEVEL)


def mysql_select(query, params):
    records = []
    logger.debug(query)
    logger.debug(params)
    try:
        cnx = mysql.connector.connect(
            host=config.DATABASE_URL,
            database=config.DATABASE_SCHEMA,
            user=config.DATABASE_USERNAME,
            password=config.DATABASE_PASSWORD)
        cursor = cnx.cursor(prepared=True)
        cursor.execute(query, params)
        for r in cursor:
            records.append(r)
        cursor.close()
        cnx.close()
        logger.debug('Results: %d', len(records))
    except Exception:
        logger.error('Error connecting to database', exc_info=True)
    return records


def mysql_modify(query, params, is_update=False):
    ret_val = 0
    logger.debug(query)
    logger.debug(params)
    try:
        cnx = mysql.connector.connect(
            host=config.DATABASE_URL,
            database=config.DATABASE_SCHEMA,
            user=config.DATABASE_USERNAME,
            password=config.DATABASE_PASSWORD)
        cursor = cnx.cursor(buffered=True)
        cursor.execute(query, params)
        cnx.commit()
        ret_val = cursor.rowcount if is_update else cursor.lastrowid
        logger.debug(f'Results: {ret_val}')
    except Exception:
        logger.error('Error connecting to database', exc_info=True)
    finally:
        cursor.close()
        cnx.close()
    return ret_val
