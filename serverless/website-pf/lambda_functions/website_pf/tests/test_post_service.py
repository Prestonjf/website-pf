# Website-PF Tests
import logging
from lambda_functions.website_pf.src import config

logger = logging.getLogger(__file__)
logger.setLevel(config.LOG_LEVEL)


def test_post_service():
    assert True
