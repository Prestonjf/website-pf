from logging import getLogger
from os import environ
from pytest import fixture
from unittest.mock import patch

environ['LOG_LEVEL'] = 'WARNING'
environ['STAGE'] = 'test'
environ['REGION'] = 'us-east-1'
environ['ACCOUNT_ID'] = '123456789012'


# Mock SSM parameter values for testing
SSM_PARAMETER_VALUES = {
    "/test/website-pf/vpc/id": "vpc-12345678",
    "/test/website-pf/vpc/subnet/id": "subnet-12345678",
    "/test/website-pf/vpc/sg/id": "sg-12345678",
    "/test/website-pf/rds/hostname": "test-db.example.com",
    "/test/website-pf/rds/schema": "website_pf",
    "/test/website-pf/rds/username": "testuser",
    "/test/website-pf/rds/password": "testpassword",
    "/test/website-pf/acm/url": "prestonfrazier.net",
    "/test/website-pf/acm/arn": "arn:aws:acm:us-east-1:123456789012:certificate/12345678",
    "/test/waf/cloudfront/arn": "arn:aws:wafv2:us-east-1:123456789012:global/webacl/test/12345678",
}


def mock_get_ssm_parameter(name: str, default_value: str = ""):
    """Mock implementation of get_ssm_parameter that returns values based on parameter name."""
    return SSM_PARAMETER_VALUES.get(name, default_value)


@fixture(scope="function")
def mock_config_ssm():
    """Fixture that patches Config.get_ssm_parameter to return test values."""
    with patch('config.Config.get_ssm_parameter', side_effect=mock_get_ssm_parameter):
        yield


@fixture(scope="function")
def logger():
    return getLogger()


pytest_plugins = [
    'tests.fixtures.cdk_mocks'
]
