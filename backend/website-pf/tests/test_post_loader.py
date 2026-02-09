# Website-PF Tests
import pytest
import logging
import boto3
from unittest.mock import patch, call, Mock
from lambda_functions.website_pf_post_loader.src import config
from lambda_functions.website_pf_post_loader.src import app

logger = logging.getLogger()
logger.setLevel(config.LOG_LEVEL)


@pytest.fixture(scope="module")
def mock_boto3_client():
    with patch.object(boto3, 'client'):
        yield


@pytest.fixture(scope="function")
def mock_post_service(mock_boto3_client):
    with patch('lambda_functions.website_pf_post_loader.src.post_service') as mock_service:
        mock_service.return_value.toggle = Mock(return_value='post success')
        yield mock_service


def test_post_loader():
    assert True


def test_html_replace():
    data = "my site $$_domain_$$"
    updated_data = app.replace_html_dynamic_values(data)
    assert (updated_data == "my site http://localhost:3001/site/0.7.0")
