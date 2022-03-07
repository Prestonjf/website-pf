# Website-PF Tests
import logging
from lambda_backend.website_pf_post_loader.src import config

logger = logging.getLogger(__file__)
logger.setLevel(config.LOG_LEVEL)


def test_post_loader():
    assert True
