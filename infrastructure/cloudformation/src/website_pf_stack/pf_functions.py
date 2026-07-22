from os.path import dirname, join

from aws_cdk import BundlingOptions, Duration, RemovalPolicy, aws_lambda
from aws_cdk.aws_ec2 import SecurityGroup, Subnet, SubnetSelection, Vpc
from aws_cdk.aws_lambda import Function, LayerVersion, RuntimeManagementMode
from constructs import Construct

import utils
from config import Config
from website_pf_stack import pf_cloudwatch, pf_iam

DEFAULT_LAMBDA_CODE = '''def lambda_handler(event, context):
    return {"statusCode": 200, "body": "OK"}'''


class WebsitePfPoetryLambdaLayer():
    """Lambda layer with shared dependencies."""

    layer: LayerVersion = None

    def __init__(self, scope: Construct, construct_id: str, config: Config, override_properties: dict = {}, pyproject_toml_dir: str = '', **kwargs):

        bundling_options = BundlingOptions(
            image=aws_lambda.Runtime.PYTHON_3_13.bundling_image,
            user="0:0",
            command=[
                "bash", "-c",
                "pip install poetry==2.2.1 && "
                "poetry install --only main --no-directory --no-root && "
                "mkdir -p /asset-output/python && "
                "rsync -a "
                "--exclude='*.pyc' "
                "--exclude='__pycache__' "
                "--exclude='*.dist-info' "
                "--exclude='.pytest_cache' "
                "--exclude='tests' "
                "/asset-input/.venv/lib*/python*/site-packages/ /asset-output/python/ || true"
            ],
            environment={
                "POETRY_VIRTUALENVS_IN_PROJECT": "true"
            }
        )

        properties = {
            'layer_version_name': f"website-pf-layer-{config.stage}",
            'removal_policy': RemovalPolicy.RETAIN,
            'compatible_runtimes': [aws_lambda.Runtime.PYTHON_3_13],
            'description': 'Lambda Layer for Website-PF application dependencies',
            'code': aws_lambda.Code.from_asset(
                pyproject_toml_dir,
                bundling=bundling_options
            )
        }

        utils.update_dictionaries(properties, override_properties)
        self.layer = LayerVersion(
            scope,
            construct_id,
            **properties
        )


class WebsitePfLambdaFunction():
    """Lambda functions for Website-PF stack."""

    function: Function = None

    def __init__(self, scope: Construct, construct_id: str, config: Config, override_properties: dict = {}, **kwargs):

        properties = {
            'function_name': f"default-website-pf-{config.stage}",
            'description': 'Default Lambda function description for website-pf',
            'handler': 'lambda_function.lambda_handler',
            'code': aws_lambda.Code.from_inline(DEFAULT_LAMBDA_CODE),
            'runtime': aws_lambda.Runtime.PYTHON_3_13,
            'runtime_management_mode': RuntimeManagementMode.FUNCTION_UPDATE,
            'allow_public_subnet': True,
            'memory_size': 256,
            'timeout': Duration.seconds(28),
            'vpc': Vpc.from_lookup(scope, f"{construct_id}Vpc", vpc_id=config.vpc_id),
            'vpc_subnets': SubnetSelection(subnets=[Subnet.from_subnet_id(scope, f"{construct_id}Subnet", subnet_id=config.vpc_subnet_id)]),
            'security_groups': [SecurityGroup.from_security_group_id(scope, f"{construct_id}Sg", security_group_id=config.vpc_sg_id)],
            'environment': {
                "LOG_LEVEL": "INFO",
                "STAGE": config.stage,
                "CUSTOMER": config.customer,
                "ENVIRONMENT": config.environment,
                "REGION": config.region,
                "VERSION": config.version
            },
        }

        utils.update_dictionaries(properties, override_properties)
        self.function = Function(
            scope,
            construct_id,
            **properties
        )


def website_pf_lambda_layer(scope: Construct, construct_id: str, config: Config, **kwargs) -> WebsitePfPoetryLambdaLayer:
    """Create Lambda layer with Poetry dependencies built in Docker using AWS Lambda Python 3.13 image."""

    pyproject_toml_dir = join(dirname(__file__), '../../../../backend/website-pf/')
    override_properties = {
        'layer_version_name': f"website-pf-layer-{config.stage}",

    }
    return WebsitePfPoetryLambdaLayer(scope, construct_id, config, override_properties, pyproject_toml_dir, **kwargs)


def website_pf_api_lambda(scope: Construct, construct_id: str, config: Config, **kwargs) -> WebsitePfLambdaFunction:
    """Factory function to create the main API Lambda function for Website-PF stack."""

    log_group_properties = {
        'log_group_name': f"/aws/lambda/{config.website_pf_api_lambda_name}"
    }
    website_pf_api_log_group = pf_cloudwatch.WebsitePfLogGroup(scope, construct_id, config, log_group_properties)
    website_pf_api_iam = pf_iam.website_pf_api_lambda_iam(scope, construct_id, config)

    override_properties = {
        'function_name': config.website_pf_api_lambda_name,
        'description': 'Main API Lambda function for Website-PF stack',
        'handler': 'website_pf_api.app.lambda_handler',
        'layers': kwargs.get('layers', []),
        'code': aws_lambda.Code.from_asset(
            join(dirname(__file__), '../../../../backend/website-pf/src/website_pf_api/'),
            exclude=["*.pyc", "**__pycache__"]
        ),
        'memory_size': 256,
        'timeout': Duration.seconds(28),
        'role': website_pf_api_iam.role,
        'log_group': website_pf_api_log_group.log_group,
        'environment': {
            "S3_WEBSITE_PF_BUCKET": config.website_pf_posts_bucket_name,
            "WEBSITE_URL": f"https://{config.domain_name}",
            "DATABASE_URL": config.db_hostname,
            "DATABASE_SCHEMA": config.db_schema,
            "DATABASE_USERNAME": config.db_username,
            "DATABASE_PASSWORD": config.db_password
        }
    }

    lambda_function = WebsitePfLambdaFunction(scope, construct_id, config, override_properties, **kwargs)
    lambda_function.function.node.add_dependency(website_pf_api_iam.policy)

    return lambda_function.function


def website_pf_post_loader_lambda(scope: Construct, construct_id: str, config: Config, **kwargs) -> WebsitePfLambdaFunction:
    """Factory function to create the post loader Lambda function for Website-PF stack."""

    log_group_properties = {
        'log_group_name': f"/aws/lambda/{config.website_pf_loader_lambda_name}"
    }
    website_pf_loader_log_group = pf_cloudwatch.WebsitePfLogGroup(scope, construct_id, config, log_group_properties)
    website_pf_loader_iam = pf_iam.website_pf_loader_lambda_iam(scope, construct_id, config)

    override_properties = {
        'function_name': config.website_pf_loader_lambda_name,
        'description': 'Post loader Lambda function for Website-PF stack',
        'handler': 'website_pf_post_loader.app.lambda_handler',
        'layers': kwargs.get('layers', []),
        'code': aws_lambda.Code.from_asset(
            join(dirname(__file__), '../../../../backend/website-pf/src/website_pf_post_loader/'),
            exclude=["*.pyc", "**__pycache__"]
        ),
        'memory_size': 256,
        'timeout': Duration.seconds(60),
        'role': website_pf_loader_iam.role,
        'log_group': website_pf_loader_log_group.log_group,
        'environment': {
            "S3_WEBSITE_PF_BUCKET": config.website_pf_posts_bucket_name,
            "WEBSITE_URL": f"https://{config.domain_name}",
            "FEATURED_POSTS": "about,portfolio",
            "DATABASE_URL": config.db_hostname,
            "DATABASE_SCHEMA": config.db_schema,
            "DATABASE_USERNAME": config.db_username,
            "DATABASE_PASSWORD": config.db_password
        }
    }

    lambda_function = WebsitePfLambdaFunction(scope, construct_id, config, override_properties, **kwargs)
    lambda_function.function.node.add_dependency(website_pf_loader_iam.policy)

    return lambda_function.function
