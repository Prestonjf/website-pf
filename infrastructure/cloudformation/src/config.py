from typing import Optional

import utils
from aws_cdk import Environment
from boto3 import client

logger = utils.setup_logging()


class Config:

    def __init__(
        self,
        stage_id: str,
        env: Environment,
        app_version: str,
        project_name: str,
        python_lambda_runtime: str = None,
    ):
        self.ssm_client = client("ssm", region_name=env.region)

        # Basic configuration
        stage_split = stage_id.split("-")
        self.stage = stage_id
        self.customer = stage_split[0]
        self.environment = stage_split[1]
        self.account_id = env.account
        self.region = env.region
        self.version = app_version
        self.project_name = project_name

        # /website-pf/api-gateway/key
        # Existing Infrastructure Configurations
        self.deployment_bucket_name = "pfrazier-cdk-deployments"
        # Route 53 / ACM configuration
        self.domain_name = self.get_ssm_parameter(f"/{self.stage}/domain/name")
        self.domain_acm_arn = self.get_ssm_parameter(f"/{self.stage}/domain/acm/arn")
        # VPC configuration
        self.vpc_id = self.get_ssm_parameter(f"/{self.stage}/vpc/id")
        self.vpc_subnet_id = self.get_ssm_parameter(f"/{self.stage}/vpc/subnet/id")
        self.vpc_sg_id = self.get_ssm_parameter(f"/{self.stage}/vpc/sg/id")
        # WAF configuration
        self.waf_cloudfront_arn = self.get_ssm_parameter(f"/{self.stage}/waf/cloudfront/arn")

        # Stack Resource Names
        self.website_pf_stack_name = f"{project_name}-{stage_id}"

        # Lambda Resource Names
        self.website_pf_api_lambda_name = f"website-pf-api-{self.stage}"
        self.website_pf_loader_lambda_name = f"website-pf-post-loader-{self.stage}"

        # CloudFront configuration
        # S3 Resource Names
        self.website_pf_webapp_bucket_name = f"website-pf-webapp-{self.stage}"
        self.website_pf_content_bucket_name = f"website-pf-content-{self.stage}"

        # CloudFront configuration

        # API Gateway configuration

        # RDS configuration
        self.db_hostname = self.get_ssm_parameter(f"/{self.stage}/website-pf/rds/hostname")
        self.db_schema = self.get_ssm_parameter(f"/{self.stage}/website-pf/rds/schema")
        self.db_username = self.get_ssm_parameter(f"/{self.stage}/website-pf/rds/username")
        self.db_password = self.get_ssm_parameter(f"/{self.stage}/website-pf/rds/password")

    def get_ssm_parameter(self, name: str, default_value: str = "") -> Optional[str]:
        """Get parameter value from SSM Parameter Store."""
        try:
            response = self.ssm_client.get_parameter(
                Name=name, WithDecryption=True
            )
            return response["Parameter"]["Value"]
        except Exception:
            logger.error(f"SSM parameter '{name}' not found.", exc_info=True)
            return default_value
