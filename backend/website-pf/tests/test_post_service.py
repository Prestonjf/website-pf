# Website-PF Tests
import logging
from website_pf_api import config

logger = logging.getLogger(__file__)
logger.setLevel(config.LOG_LEVEL)


def test_post_service():
    assert True
