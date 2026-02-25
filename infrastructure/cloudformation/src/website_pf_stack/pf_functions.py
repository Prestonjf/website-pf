"""
Lambda functions and layers for Website-PF stack.
"""
import os
from constructs import Construct
from aws_cdk import Duration, RemovalPolicy
from aws_cdk import aws_lambda
from aws_cdk.aws_lambda import Function, LayerVersion, RuntimeManagementMode
from aws_cdk.aws_ec2 import SecurityGroup, Vpc, Subnet, SubnetSelection
import utils
from config import Config
from website_pf_stack import pf_cloudfront, pf_iam, pf_cloudwatch


class WebsitePfLambdaLayer():
    """Lambda layer with shared dependencies."""

    layer = None

    def __init__(self, scope: Construct, construct_id: str, config: Config, override_properties: dict = {}, **kwargs):

        properties = {
            'layer_version_name': f"website-pf-layer-{config.stage}",
            'removal_policy': RemovalPolicy.RETAIN,
            'compatible_runtimes': [aws_lambda.Runtime.PYTHON_3_13],
            'description': 'Lambda Layer for Website-PF application dependencies',
            # TODO: Set Asset path
            'code': aws_lambda.Code.from_asset(os.path.join(os.path.dirname(__file__), ""))
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
            'handler': 'index.handler',
            'code': aws_lambda.Code.from_asset(os.path.join(os.path.dirname(__file__), "")),

            'runtime': aws_lambda.Runtime.PYTHON_3_13,
            'runtime_management_mode': RuntimeManagementMode.FUNCTION_UPDATE,
            #'role': self.iam_role.role,
            #'log_group': self.log_group.log_group,
            'memory_size': 256,
            'timeout': Duration.seconds(28),
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
