# MySQL Services.
import config
import logging
import mysql.connector

logger = logging.getLogger('app.repositories.mysql_repository')
logger.setLevel(config.LOG_LEVEL)


def mysql_select(query, params):
    records = []
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
        logger.debug(records)
        cursor.close()
        cnx.close()
    except Exception:
        logger.error('Error connecting to database', exc_info=True)
    return records
