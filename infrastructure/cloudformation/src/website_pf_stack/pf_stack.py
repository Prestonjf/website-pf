import aws_cdk as cdk
from aws_cdk import Stack
from constructs import Construct
from website_pf_stack import pf_apigateway, pf_cloudfront, pf_functions

from config import Config


class WebsitePfStack(Stack):
    """Main stack for Website-PF infrastructure."""

    def __init__(self, scope: Construct, construct_id: str, config: Config, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        cdk.Tags.of(self).add("Component", config.project_name)

        website_pf_lambda_layer = pf_functions.website_pf_lambda_layer(self, "WebsitePfLambdaLayer", config)
        website_pf_api_lambda = pf_functions.website_pf_api_lambda(self, "WebsitePfApiLambda", config, layers=[website_pf_lambda_layer.layer])
        _ = pf_functions.website_pf_post_loader_lambda(self, "WebsitePfPostLoaderLambda", config, layers=[website_pf_lambda_layer.layer])

        _ = pf_apigateway.website_pf_rest_api(self, "WebsitePfApi", config, lambda_handler_function=website_pf_api_lambda)

        _ = pf_cloudfront.website_pf_cloudfront(self, "WebsitePfCloudFront", config)
