from aws_cdk import App, Environment
from aws_cdk.core import CliCredentialsStackSynthesizer
from logging import Logger, getLogger, StreamHandler, Formatter, ERROR
from pythonjsonlogger.json import JsonFormatter
from os import getenv


logger = getLogger("website_pf")


def get_stage_environment(app: App):

    environments = {
        "prod": {"account_id": "", "region": "us-east-1"}
    }

    stage_name = app.node.try_get_context("stage_name")
    env = environments.get(stage_name)

    if stage_name and env:
        logger.info(f"Found stage '{stage_name}' with environment: {env}")
        return stage_name, Environment(account=env["account_id"], region=env["region"]) 
    else:
        logger.warning(f"No stage or environment found in context for stage_name '{stage_name}'.")
        return None, None


def setup_logging(logger: Logger, json_format: bool = True):

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


def get_stack_synthesizer(config, stack_name: str) -> CliCredentialsStackSynthesizer:
    """
    Create and return a CliCredentialsStackSynthesizer for stack synthesis.

    Returns:
        CliCredentialsStackSynthesizer: Configured stack synthesizer using CLI credentials
    """
    return CliCredentialsStackSynthesizer()


setup_logging(logger)
