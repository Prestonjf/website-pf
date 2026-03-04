"""
Lambda functions and layers for Website-PF stack.
"""
from constructs import Construct
from aws_cdk import Duration, RemovalPolicy, BundlingOptions
from aws_cdk import aws_lambda
from aws_cdk.aws_lambda import Function, LayerVersion, RuntimeManagementMode
from aws_cdk.aws_ec2 import SecurityGroup, Vpc, Subnet, SubnetSelection
import utils
from os.path import join, dirname
from config import Config
from website_pf_stack import pf_cloudfront, pf_iam, pf_cloudwatch


DEFAULT_LAMBDA_CODE = '''def lambda_handler(event, context):
    return {"statusCode": 200, "body": "OK"}'''


class WebsitePfPoetryLambdaLayer():
    """Lambda layer with shared dependencies."""

    layer = None

    def __init__(self, scope: Construct, construct_id: str, config: Config, override_properties: dict = {}, pyproject_toml_dir: str = '', **kwargs):

        bundling_options = BundlingOptions(
            image=aws_lambda.Runtime.PYTHON_3_13.bundling_image,
            user="0:0",
            command=[
                "bash", "-c",
                "pip install poetry && "
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

    function = None
    log_group = None
    iam_role = None

    def __init__(self, scope: Construct, construct_id: str, config: Config, override_properties: dict = {}, **kwargs):

        log_group_properties = {
            'log_group_name': f"/aws/lambda/{override_properties.get('function_name')}-{config.stage}"
        }
        self.log_group = None
        self.iam_role = None

        properties = {
            'function_name': f"default-website-pf-{config.stage}",
            'description': 'Default Lambda function description for website-pf',
            'handler': 'lambda_function.lambda_handler',
            'code': aws_lambda.Code.from_inline(DEFAULT_LAMBDA_CODE),
            'runtime': aws_lambda.Runtime.PYTHON_3_13,
            'runtime_management_mode': RuntimeManagementMode.FUNCTION_UPDATE,
            #'role': self.iam_role.role,
            #'log_group': self.log_group.log_group,
            'memory_size': 256,
            'timeout': Duration.seconds(28),
            'allow_public_subnet': True,
            'vpc': Vpc.from_lookup(scope, f"{construct_id}Vpc", vpc_id=config.vpc_id),
            'vpc_subnets': SubnetSelection(subnets=[Subnet.from_subnet_id(scope, f"{construct_id}Subnet", subnet_id=config.vpc_subnet_id)]),
            'security_groups': [SecurityGroup.from_security_group_id(scope, f"{construct_id}Sg", security_group_id=config.vpc_sg_id)],
            'environment': {
                "LOG_LEVEL": "INFO",
                "STAGE": config.stage,
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
    return WebsitePfPoetryLambdaLayer(scope, construct_id, config, override_properties, pyproject_toml_dir,  **kwargs)


def website_pf_api_lambda(scope: Construct, construct_id: str, config: Config, **kwargs) -> WebsitePfLambdaFunction:
    """Factory function to create the main API Lambda function for Website-PF stack."""

    override_properties = {
        'function_name': f"website-pf-api-{config.stage}",
        'description': 'Main API Lambda function for Website-PF stack',
        'handler': 'website_pf_api.app.lambda_handler',
        'layers': kwargs.get('layers', []),
        'code': aws_lambda.Code.from_asset(
            join(dirname(__file__), '../../../../backend/website-pf/src/website_pf_api/'),
            exclude=["*.pyc", "**__pycache__"]
        ),
    }

    return WebsitePfLambdaFunction(scope, construct_id, config, override_properties, **kwargs)
