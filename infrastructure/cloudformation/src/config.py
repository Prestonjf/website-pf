"""
Configuration for Website-PF CDK application.
"""
from aws_cdk import Environment
from boto3 import client
from typing import Optional
from src import utils


logger = utils.setup_logging()


class Config:
    """Base configuration class."""

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
        self.stage = stage_id
        self.account_id = env.account
        self.region = env.region
        self.version = app_version
        self.project_name = project_name

        # Stack Resource Names
        self.website_pf_stack_name = f"{project_name}-{stage_id}"

        # S3 configuration
        self.s3_bucket_name = f"{project_name}-{stage_id}"

        # Lambda configuration
        self.lambda_runtime = python_lambda_runtime or "python3.13"
        self.lambda_memory_api = 256
        self.lambda_timeout_api = 10
        self.lambda_memory_post_loader = 256
        self.lambda_timeout_post_loader = 30

        # CloudFront configuration
        self.cloudfront_aliases = ["prestonfrazier.net", "www.prestonfrazier.net"]
        self.cloudfront_price_class = "PriceClass_100"
        self.cloudfront_cache_default_ttl = 86400
        self.cloudfront_cache_max_ttl = 31536000
        self.cloudfront_cache_min_ttl = 1

        # API Gateway configuration
        self.api_key_name = f"website-pf-{stage_id}-client-key-111112"
        self.api_key_description = "Client key for website-pf api application."
        self.api_usage_plan_quota_limit = 40001
        self.api_usage_plan_quota_period = "DAY"
        self.api_usage_plan_burst_limit = 10
        self.api_usage_plan_rate_limit = 20

        # VPC configuration
        self.vpc_sg_id = self.get_ssm_parameter(f"/{stage_id}/website-pf/vpc/sg/id")
        self.vpc_subnet_id = self.get_ssm_parameter(f"/{stage_id}/website-pf/vpc/subnet/id")
        self.vpc_id = self.get_ssm_parameter(f"/{stage_id}/website-pf/vpc/id")

        # RDS configuration
        self.db_hostname = self.get_ssm_parameter(f"/{stage_id}/website-pf/rds/hostname")
        self.db_schema = self.get_ssm_parameter(f"/{stage_id}/website-pf/rds/schema")
        self.db_username = self.get_ssm_parameter(f"/{stage_id}/website-pf/rds/username")
        self.db_password = self.get_ssm_parameter(f"/{stage_id}/website-pf/rds/password")

        # ACM configuration
        self.acm_url = self.get_ssm_parameter(f"/{stage_id}/website-pf/acm/url")
        self.acm_arn = self.get_ssm_parameter(f"/{stage_id}/website-pf/acm/arn")

        # WAF configuration
        self.waf_cloudfront_arn = self.get_ssm_parameter(f"/{stage_id}/waf/cloudfront/arn")

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
