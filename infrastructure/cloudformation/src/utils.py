from aws_cdk import App, Environment, CliCredentialsStackSynthesizer
from logging import Logger, getLogger, StreamHandler, Formatter, ERROR
from pythonjsonlogger.json import JsonFormatter
from os import getenv, getcwd
from os.path import exists, join, getsize
import subprocess
import shutil


logger = getLogger("website_pf")
WORK_DIR = './requirements'


class CustomSynthesizer(CliCredentialsStackSynthesizer):

    def __init__(self, stage_name: str, project_name: str, bucket_name: str, version: str, stack_name: str):

        if not all([stage_name, project_name, bucket_name, version, stack_name]):
            raise ValueError("All parameters must be provided and non-empty.")

        s3_prefix = f"{stage_name}/{project_name}/{stack_name}/{version}/"

        super().__init__(
            file_assets_bucket_name=bucket_name,
            bucket_prefix=s3_prefix,
            qualifier=""
        )


def get_stack_synthesizer(config, stack_name: str) -> CliCredentialsStackSynthesizer:
    """
    Create and return a CliCredentialsStackSynthesizer for stack synthesis.

    Returns:
        CliCredentialsStackSynthesizer: Configured stack synthesizer using CLI credentials
    """
    return CustomSynthesizer(
        stage_name=config.stage,
        project_name=config.project_name,
        bucket_name=config.deployment_bucket_name,
        version=config.version,
        stack_name=stack_name
    )


def get_stage_environment(app: App):

    environments = {
        "prod": {"account_id": "890384337971", "region": "us-east-1"}
    }

    stage_name = app.node.try_get_context("stage_name")
    env = environments.get(stage_name)

    if stage_name and env:
        logger.info(f"Found stage '{stage_name}' with environment: {env}")
        return stage_name, Environment(account=env["account_id"], region=env["region"])
    else:
        logger.warning(f"No stage or environment found in context for stage_name '{stage_name}'.")
        return None, None


def update_dictionaries(dict1: dict, dict2: dict) -> dict:

    for key, value in dict2.items():
        if key in dict1 and isinstance(dict1[key], dict) and isinstance(value, dict):
            dict1[key] = update_dictionaries(dict1[key], value)
        else:
            dict1[key] = value
    return dict1


def setup_logging(logger: Logger = None, json_format: bool = True):

    if logger is None:
        logger = getLogger("website_pf")

    for h in logger.handlers:
        logger.removeHandler(h)

    stream_handler = StreamHandler()

    if json_format:
        stream_handler.setFormatter(
            JsonFormatter(("%(levelname)s %(message)s %(funcName)s %(asctime)s %(exc_info)s %(name)s %(pathname)s %(args)s"))
        )
    else:
        stream_handler.setFormatter(Formatter("%(asctime)s %(levelname)s %(message)s"))

    logger.addHandler(stream_handler)
    logger.setLevel(getenv("LOG_LEVEL", "INFO"))
    logger.propagate = False

    getLogger('boto3').setLevel(ERROR)
    getLogger('botocore').setLevel(ERROR)
    getLogger('aws_xray_sdk').setLevel(ERROR)
    getLogger('urllib3').setLevel(ERROR)
    getLogger('requests').setLevel(ERROR)
    getLogger('mysql.connector').setLevel(ERROR)

    return logger


setup_logging(logger)
