"""
Website-PF CDK Stack.
"""
from constructs import Construct
import aws_cdk as cdk
from aws_cdk import aws_ec2, Stack, App, CfnOutput
from website_pf_stack import pf_functions
from config import Config


class WebsitePfStack(Stack):
    """Main stack for Website-PF infrastructure."""

    def __init__(self, scope: Construct, construct_id: str, config: Config, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        cdk.Tags.of(self).add("Component", config.website_pf_stack_name)

        lambda_layer = pf_functions.website_pf_lambda_layer(self, "WebsitePfLambdaLayer", config)
        website_pf_api_lambda = pf_functions.website_pf_api_lambda(self, "WebsitePfApiLambda", config, layers=[lambda_layer.layer])

    #     environment_vars = {
    #         "LOG_LEVEL": "INFO",
    #         "ENVIRONMENT": stage,
    #         "REGION": region,
    #         "VERSION": version,
    #         "WEBSITE_URL": self._get_ssm_parameter(f"/{stage}/website-pf/acm/url"),
    #         "S3_WEBSITE_PF_BUCKET": f"website-pf-{stage}",
    #         "DATABASE_URL": self._get_ssm_parameter(f"/{stage}/website-pf/rds/hostname"),
    #         "DATABASE_SCHEMA": self._get_ssm_parameter(f"/{stage}/website-pf/rds/schema"),
    #         "DATABASE_USERNAME": self._get_ssm_parameter(f"/{stage}/website-pf/rds/username"),
    #         "DATABASE_PASSWORD": self._get_ssm_parameter(f"/{stage}/website-pf/rds/password"),
    #     }

    #     # VPC configuration
    #     vpc_config = self._get_vpc_config(stage)

    #     # ACM configuration
    #     acm_config = {
    #         "arn": self._get_ssm_parameter(f"/{stage}/website-pf/acm/arn"),
    #         "url": self._get_ssm_parameter(f"/{stage}/website-pf/acm/url"),
    #     }

    #     # WAF configuration
    #     waf_config = {
    #         "arn": self._get_ssm_parameter(f"/{stage}/waf/cloudfront/arn"),
    #     }

    #     # Create IAM roles
    #     iam = WebsitePFIAM(self, "IAM")

    #     # Create Lambda layer
    #     lambda_layer = functions.WebsitePFLambdaLayer(self, "LambdaLayer")

    #     # Create Lambda functions
    #     lambda_functions = functions.WebsitePFLambdaFunctions(
    #         self,
    #         "LambdaFunctions",
    #         lambda_role=iam.lambda_role,
    #         layer=lambda_layer.layer,
    #         stage=stage,
    #         environment_vars=environment_vars,
    #         vpc_config=vpc_config,
    #     )

    #     # Create CloudFront distribution
    #     cloudfront = cloudfront.WebsitePFCloudFront(
    #         self,
    #         "CloudFront",
    #         stage=stage,
    #         version=version,
    #         acm_config=acm_config,
    #         waf_config=waf_config,
    #     )

    # def _get_ssm_parameter(self, parameter_name: str) -> str:
    #     """
    #     Get SSM parameter value.
    #     Returns placeholder in format that can be resolved at deploy time.
    #     """
    #     return f"{{{{ssm:{parameter_name}}}}}"

    # def _get_vpc_config(self, stage: str) -> dict:
    #     """
    #     Get VPC configuration from context or SSM.
    #     """
    #     vpc_sg_id = self.node.try_get_context(f"{stage}_vpc_sg_id") or self._get_ssm_parameter(
    #         f"/{stage}/website-pf/vpc/sg/id"
    #     )
    #     vpc_subnet_id = self.node.try_get_context(f"{stage}_vpc_subnet_id") or self._get_ssm_parameter(
    #         f"/{stage}/website-pf/vpc/subnet/id"
    #     )

    #     # For actual VPC usage, retrieve subnets from existing VPC
    #     # This is a simplified version - in production, you'd likely look up existing VPC
    #     vpc_id = self.node.try_get_context(f"{stage}_vpc_id") or self._get_ssm_parameter(
    #         f"/{stage}/website-pf/vpc/id"
    #     )

    #     return {
    #         "security_group": ec2.SecurityGroup.from_security_group_id(
    #             self,
    #             "WebsitePFSecurityGroup",
    #             security_group_id=vpc_sg_id,
    #         ),
    #         "subnet": ec2.Subnet.from_subnet_attributes(
    #             self,
    #             "WebsitePFSubnet",
    #             subnet_id=vpc_subnet_id,
    #             availability_zone="us-east-1a",  # Can be made configurable
    #         ),
    #     }
