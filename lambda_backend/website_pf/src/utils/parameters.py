import boto3
import logging
import config

logger = logging.getLogger(__file__)
logger.setLevel(config.LOG_LEVEL)


class Parameters:

    __instance = None

    @staticmethod
    def getInstance():
        if Parameters.__instance is None:
            Parameters()
        return Parameters.__instance

    def __init__(self):
        client = boto3.client('ssm')
        p = {}
        logger.info('getting singelton')
        # p['website-pf-mysql-url'] = getParameter('website-pf-mysql-url', client)
        # p['website-pf-mysql-username'] = getParameter('website-pf-mysql-username', client)
        # p['website-pf-password'] = getParameter('website-pf-password', client)
        # p['website-pf-database'] = getParameter('website-pf-database', client)
        logger.debug(p)
        Parameters.__instance = p


def getParameter(name, client):
    client = boto3.client('ssm')
    return client.get_parameter(Name=name, WithDecryption=True)['Parameter']['Value']
