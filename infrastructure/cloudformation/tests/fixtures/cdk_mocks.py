from pytest import fixture
from os import getenv
from unittest.mock import MagicMock
from aws_cdk import App, Stack, Stage, Environment
from config import Config

Config.ssm_client = MagicMock(return_value='mock-ssm-value')


@fixture(scope="function")
def mock_cdk_app():
    return App(context={"stage_name": getenv("STAGE", "test")})


@fixture(scope="function")
def mock_cdk_env():
    return Environment(account=getenv("ACCOUNT_ID", "123456789012"), region=getenv("REGION", "us-east-1"))