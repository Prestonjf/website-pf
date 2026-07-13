"""
API Gateway constructs for Website-PF stack.
"""

from constructs import Construct
from aws_cdk import aws_apigateway, aws_certificatemanager, aws_route53
from aws_cdk.aws_apigateway import (
    RestApi,
    LogGroupLogDestination,
    AccessLogFormat,
    ApiKey,
    UsagePlan,
    MethodLoggingLevel,
    ThrottleSettings,
    QuotaSettings,
    Period,
    LambdaIntegration,
    CorsOptions,
    MockIntegration,
    IntegrationResponse,
    MethodOptions,
    MethodResponse
)
from aws_cdk.aws_certificatemanager import Certificate
from aws_cdk.aws_route53_targets import ApiGatewayDomainNameTarget
from typing import Optional
import utils
from config import Config
from website_pf_stack import pf_cloudwatch


class WebsitePfRestApi:
    """Constructs for REST API Gateway with optional certificate and custom domain."""

    api: RestApi = None
    domain_name: Optional[aws_apigateway.DomainName] = None

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        config: Config,
        override_properties: dict = {},
        sub_domain: str = None,
        **kwargs,
    ):
        """
        Initialize REST API Gateway.

        Args:
            scope: CDK scope
            construct_id: Construct ID
            config: Configuration object
            lambda_handler: Lambda function to integrate with the API
            override_properties: Additional properties to override defaults
            sub_domain: Optional subdomain for custom domain name (e.g., 'api')
            **kwargs: Additional keyword arguments
        """

        # Create log group for the API Gateway
        log_group_properties = {
            "log_group_name": f"/aws/apigateway/website-pf-{config.stage}"
        }
        api_log_group = pf_cloudwatch.WebsitePfLogGroup(scope, construct_id, config, log_group_properties)

        # Base API Gateway properties
        properties = {
            "rest_api_name": f"website-pf-{config.stage}",
            "description": "REST API Gateway for Website-PF stack",
            "deploy": True,
            "disable_execute_api_endpoint": bool(sub_domain),
            "deploy_options": aws_apigateway.StageOptions(
                stage_name=config.stage,
                logging_level=MethodLoggingLevel.INFO,
                data_trace_enabled=False,
                access_log_destination=LogGroupLogDestination(api_log_group.log_group),
                access_log_format=AccessLogFormat.clf(),
            ),
            "endpoint_types": [aws_apigateway.EndpointType.REGIONAL],
            "default_cors_preflight_options": CorsOptions(
                allow_origins=["*"],
                allow_methods=["OPTIONS", "GET"],
                allow_headers=[
                    "Content-Type",
                    "X-Amz-Date",
                    "Authorization",
                    "X-Api-Key",
                    "X-Amz-Security-Token",
                    "X-Amz-User-Agent",
                ],
                allow_credentials=True,
            )
        }

        utils.update_dictionaries(properties, override_properties)

        # Create REST API
        self.api = RestApi(scope, f"{construct_id}Gateway", **properties)

        # Add custom domain and ACM certificate if sub_domain is provided
        if sub_domain:
            self._add_custom_domain(scope, construct_id, config, sub_domain)

    def _add_custom_domain(self, scope: Construct, construct_id: str, config: Config, sub_domain: str):
        """
        Add custom domain name with ACM certificate to the API Gateway.

        Args:
            scope: CDK scope
            construct_id: Construct ID
            config: Configuration object
            sub_domain: Subdomain to use (e.g., 'api')
        """

        # Construct the full domain name
        full_domain_name = f"{sub_domain}.{config.domain_name}"

        # Create ACM certificate
        certificate = Certificate(
            scope,
            f"{construct_id}Certificate",
            domain_name=full_domain_name,
            validation=aws_certificatemanager.CertificateValidation.from_dns(
                hosted_zone=None  # Will use default hosted zone lookup
            ),
        )

        # Add custom domain name to API Gateway
        self.domain_name = self.api.add_domain_name(
            f"{construct_id}DomainName",
            domain_name=full_domain_name,
            certificate=certificate,
            security_policy=aws_apigateway.SecurityPolicy.SecurityPolicy_TLS13_1_2_2021_06,
        )

        # Create Route53 A and AAAA records for the custom API domain
        hosted_zone = aws_route53.HostedZone.from_lookup(
            scope,
            f"{construct_id}HostedZone",
            domain_name=config.domain_name,
        )

        aws_route53.ARecord(
            scope,
            f"{construct_id}ARecord",
            zone=hosted_zone,
            record_name=full_domain_name,
            target=aws_route53.RecordTarget.from_alias(
                ApiGatewayDomainNameTarget(self.domain_name)
            )
        )

        aws_route53.AaaaRecord(
            scope,
            f"{construct_id}AaaaRecord",
            zone=hosted_zone,
            record_name=full_domain_name,
            target=aws_route53.RecordTarget.from_alias(
                ApiGatewayDomainNameTarget(self.domain_name)
            )
        )


def website_pf_rest_api(
    scope: Construct,
    construct_id: str,
    config: Config,
    lambda_handler_function: object = None,
    **kwargs
) -> WebsitePfRestApi:
    """
    Factory function to create the REST API Gateway for Website-PF stack.

    Args:
        scope: CDK scope
        construct_id: Construct ID
        config: Configuration object
        lambda_handler: Lambda function to integrate with the API
        sub_domain: Optional subdomain for custom domain name
        **kwargs: Additional keyword arguments

    Returns:
        RestApi: The constructed REST API Gateway
    """

    api_gateway = WebsitePfRestApi(scope, construct_id, config, sub_domain="api", **kwargs)

    # Define API key name
    api_key_name = f"website-pf-{config.stage}-client-key-111113"

    # Create API Key
    api_key = ApiKey(
        scope,
        f"{construct_id}ApiKey",
        description="Client key for website-pf api application.",
        api_key_name=api_key_name,
    )

    # Create Usage Plan
    usage_plan = UsagePlan(
        scope,
        f"{construct_id}UsagePlan",
        name=f"website-pf-{config.stage}-usage-plan",
        description="Usage plan for website-pf api application.",
        throttle=ThrottleSettings(burst_limit=10, rate_limit=20),
        quota=QuotaSettings(limit=40001, offset=0, period=Period.DAY)
    )

    # Add API Key to Usage Plan
    usage_plan.add_api_key(api_key)

    # Add proxy integration methods if lambda_handler_function is provided
    if lambda_handler_function:
        lambda_integration = LambdaIntegration(lambda_handler_function)

        # Setup mock integration for OPTIONS methods
        mock_integration = MockIntegration(
            integration_responses=[
                IntegrationResponse(
                    status_code="200",
                    response_parameters={
                        "method.response.header.Access-Control-Allow-Headers": "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,X-Amz-User-Agent'",
                        "method.response.header.Access-Control-Allow-Methods": "'OPTIONS,GET'",
                        "method.response.header.Access-Control-Allow-Origin": "'*'",
                    },
                )
            ]
        )

        # Setup CORS options for OPTIONS methods
        cors_options = MethodOptions(
            method_responses=[
                MethodResponse(
                    status_code="200",
                    response_parameters={
                        "method.response.header.Access-Control-Allow-Headers": True,
                        "method.response.header.Access-Control-Allow-Methods": True,
                        "method.response.header.Access-Control-Allow-Origin": True,
                    },
                )
            ]
        )

        # /posts resource
        posts_resource = api_gateway.api.root.add_resource("posts")

        # /posts/recent
        recent_resource = posts_resource.add_resource("recent")
        _ = recent_resource.add_method("GET", lambda_integration, api_key_required=True)
        _ = recent_resource.add_method("OPTIONS", mock_integration, cors_options=cors_options)

        # /posts/search
        search_resource = posts_resource.add_resource("search")
        _ = search_resource.add_method("GET", lambda_integration, api_key_required=True)
        _ = search_resource.add_method("OPTIONS", mock_integration, cors_options=cors_options)

        # /posts/tags
        tags_resource = posts_resource.add_resource("tags")
        _ = tags_resource.add_method("GET", lambda_integration, api_key_required=True)
        _ = tags_resource.add_method("OPTIONS", mock_integration, cors_options=cors_options)

        # /posts/tags/{proxy+}
        tags_proxy_resource = tags_resource.add_resource("{proxy+}")
        _ = tags_proxy_resource.add_method("GET", lambda_integration, api_key_required=True)
        _ = tags_proxy_resource.add_method("OPTIONS", mock_integration, cors_options=cors_options)

        # /post resource
        post_resource = api_gateway.api.root.add_resource("post")

        # /post/{proxy+}
        post_proxy_resource = post_resource.add_resource("{proxy+}")
        _ = post_proxy_resource.add_method("GET", lambda_integration, api_key_required=True)
        _ = post_proxy_resource.add_method("OPTIONS", mock_integration, cors_options=cors_options)

    # Store API key name in SSM Parameter Store as SecureString
    _ = utils.add_ssm_parameter(
        scope,
        f"{construct_id}ApiKey",
        parameter_name=f"/{config.stage}/website-pf/api-gateway/key",
        value=api_key_name,
        description="API Gateway key for website-pf application."
    )

    # Store API domain URL in SSM Parameter Store
    _ = utils.add_ssm_parameter(
        scope,
        f"{construct_id}ApiDomainUrlParameter",
        parameter_name=f"/{config.stage}/website-pf/api-gateway/url",
        value=f"https://api.{config.domain_name}",
        description="API Gateway domain URL for website-pf application."
    )

    return api_gateway
