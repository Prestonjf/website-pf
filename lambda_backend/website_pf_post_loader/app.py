# Python Lambda App
from lambda_backend.website_pf_post_loader import config
import logging


logger = logging.getLogger('app')
logger.setLevel(config.LOG_LEVEL)


def lambda_handler(event, context):
    logger.info('Begin Website-PF post processing.')

    # uploads folder: config.yml, post file, and asset files.
    # config has mode CREATE or UPDATE

    # Traverse uploads folder and process each sub folder
    # If update check for existing post in db based on post_url (id)
        # process update updated time
        # process new post html
        # process new post image

    # If create generate new s3 path

    # post html needs version bump
    # process meta data into database
    # process html to replace links to hostname
    # Put assets in s3 posts/ folder
    # config.yml cach control = 0
    # post


    # Generate new rss.xml, sitemap.xml, cache control = 0

    logger.info('Finished Website-PF post processing.')
    return 'done'
