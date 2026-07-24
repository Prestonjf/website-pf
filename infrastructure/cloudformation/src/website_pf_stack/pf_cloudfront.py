from aws_cdk import Duration, aws_certificatemanager
from aws_cdk import aws_cloudfront as cloudfront
from aws_cdk import aws_cloudfront_origins as origins
from aws_cdk import aws_iam
from aws_cdk import aws_route53 as route53
from aws_cdk.aws_route53_targets import CloudFrontTarget
from aws_cdk.aws_s3 import BlockPublicAccess, Bucket, BucketEncryption
from constructs import Construct

import utils
from config import Config


class WebsitePfCloudFront:
    """CloudFront distribution for Website-PF."""

    webapp_bucket = None
    content_bucket = None
    distribution = None

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        config: Config,
        override_properties: dict = {},
        **kwargs,
    ):

        # S3 bucket for website UI
        self.webapp_bucket = Bucket(
            scope,
            "WebsitePfWebappBucket",
            bucket_name=config.website_pf_webapp_bucket_name,
            block_public_access=BlockPublicAccess.BLOCK_ALL,
            encryption=BucketEncryption.S3_MANAGED,
        )

        # S3 bucket for website content (posts)
        self.content_bucket = Bucket(
            scope,
            "WebsitePfContentBucket",
            bucket_name=config.website_pf_content_bucket_name,
            block_public_access=BlockPublicAccess.BLOCK_ALL,
            encryption=BucketEncryption.S3_MANAGED,
        )

        # CloudFront Origin Access Control
        oac = cloudfront.S3OriginAccessControl(
            scope,
            "WebsitePfOAC",
            origin_access_control_name=f"website-pf-access-control-{config.stage}",
        )

        # Cache policy
        cache_policy = cloudfront.CachePolicy(
            scope,
            "WebsitePfCachePolicy",
            cache_policy_name=f"website-pf-cache-policy-{config.stage}",
            default_ttl=Duration.days(1),
            max_ttl=Duration.days(365),
            min_ttl=Duration.seconds(1),
            enable_accept_encoding_brotli=True,
            enable_accept_encoding_gzip=True,
        )

        # Origin request policy
        origin_request_policy = cloudfront.OriginRequestPolicy(
            scope,
            "WebsitePfOriginRequestPolicy",
            origin_request_policy_name=f"website-pf-origin-request-policy-{config.stage}",
            header_behavior=cloudfront.OriginRequestHeaderBehavior.allow_list(
                "origin", "access-control-request-headers", "access-control-request-method"
            ),
        )

        # Response headers policy for CORS on config/media/post assets
        response_headers_policy = cloudfront.ResponseHeadersPolicy(
            scope,
            "WebsitePfResponseHeadersPolicy",
            response_headers_policy_name=f"website-pf-response-headers-policy-{config.stage}",
            cors_behavior=cloudfront.ResponseHeadersCorsBehavior(
                access_control_allow_credentials=False,
                access_control_allow_origins=["*"],
                access_control_allow_methods=["GET", "HEAD", "OPTIONS"],
                access_control_allow_headers=["*"],
                access_control_max_age=Duration.seconds(600),
                origin_override=False,
            ),
        )

        # Determine domain names based on environment
        if config.environment == "prod":
            domain_names = [config.domain_name, f"www.{config.domain_name}"]
        else:
            domain_names = [f"{config.environment}.{config.domain_name}", f"www.{config.environment}.{config.domain_name}"]

        s3_default_behavior = cloudfront.BehaviorOptions(
            origin=origins.S3BucketOrigin(
                self.webapp_bucket,
                origin_access_control_id=oac.origin_access_control_id,
                origin_id=f"website-pf-webapp-origin-{config.stage}",
            ),
            cache_policy=cache_policy,
            origin_request_policy=origin_request_policy,
            viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            response_headers_policy=response_headers_policy,
        )

        s3_content_behavior = cloudfront.BehaviorOptions(
            origin=origins.S3BucketOrigin(
                self.content_bucket,
                origin_access_control_id=oac.origin_access_control_id,
                origin_id=f"website-pf-content-origin-{config.stage}",
            ),
            cache_policy=cache_policy,
            origin_request_policy=origin_request_policy,
            viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            response_headers_policy=response_headers_policy,
        )

        properties = {
            "default_root_object": f"site/{config.version}/index.html",
            "default_behavior": s3_default_behavior,
            "additional_behaviors": {"media/*": s3_content_behavior, "config/*": s3_content_behavior, "posts/*": s3_content_behavior},
            "error_responses": [
                cloudfront.ErrorResponse(
                    http_status=403,
                    response_http_status=200,
                    response_page_path=f"/site/{config.version}/index.html",
                ),
                cloudfront.ErrorResponse(
                    http_status=404,
                    response_http_status=200,
                    response_page_path=f"/site/{config.version}/index.html",
                ),
            ],
            "domain_names": domain_names,
            "web_acl_id": config.waf_cloudfront_arn if config.waf_cloudfront_arn else None,
            "price_class": cloudfront.PriceClass.PRICE_CLASS_100,
            "comment": f"Website-Pf {config.stage} distribution",
        }

        if config.environment == "prod":
            if config.domain_acm_arn:
                properties["certificate"] = aws_certificatemanager.Certificate.from_certificate_arn(
                    scope,
                    "WebsitePfCloudfrontCertificate",
                    certificate_arn=config.domain_acm_arn,
                )
        else:
            # Create new ACM certificate for non-prod environments
            certificate = aws_certificatemanager.Certificate(
                scope,
                "WebsitePfCloudfrontCertificate",
                domain_name=domain_names[0],
                subject_alternative_names=domain_names[1:] if len(domain_names) > 1 else [],
            )
            properties["certificate"] = certificate

        utils.update_dictionaries(properties, override_properties)

        # CloudFront distribution
        self.distribution = cloudfront.Distribution(scope, "WebsitePfCloudfrontDistribution", **properties)

        # Add S3 bucket policy to allow read access from CloudFront OAC
        self.webapp_bucket.add_to_resource_policy(
            aws_iam.PolicyStatement(
                sid="OACReadGetObjects",
                effect=aws_iam.Effect.ALLOW,
                principals=[aws_iam.ServicePrincipal("cloudfront.amazonaws.com")],
                actions=["s3:GetObject"],
                conditions={
                    "StringEquals": {
                        "AWS:SourceArn": f"arn:aws:cloudfront::{config.account_id}:distribution/{self.distribution.distribution_id}"
                    }
                },
                resources=[f"{self.webapp_bucket.bucket_arn}/*"],
            )
        )
        self.content_bucket.add_to_resource_policy(
            aws_iam.PolicyStatement(
                sid="OACReadGetObjects",
                effect=aws_iam.Effect.ALLOW,
                principals=[aws_iam.ServicePrincipal("cloudfront.amazonaws.com")],
                actions=["s3:GetObject"],
                conditions={
                    "StringEquals": {
                        "AWS:SourceArn": f"arn:aws:cloudfront::{config.account_id}:distribution/{self.distribution.distribution_id}"
                    }
                },
                resources=[f"{self.content_bucket.bucket_arn}/*"],
            )
        )

        # Look up the hosted zone
        hosted_zone = route53.HostedZone.from_lookup(
            scope,
            "WebsitePfHostedZone",
            domain_name=config.domain_name,
        )

        # Create Route53 A and AAAA records for each domain name
        for idx, domain in enumerate(domain_names):
            # A record
            route53.ARecord(
                scope,
                f"WebsitePfARecord{idx}",
                zone=hosted_zone,
                record_name=domain,
                target=route53.RecordTarget.from_alias(CloudFrontTarget(self.distribution)),
            )
            # AAAA record
            route53.AaaaRecord(
                scope,
                f"WebsitePfAaaaRecord{idx}",
                zone=hosted_zone,
                record_name=domain,
                target=route53.RecordTarget.from_alias(CloudFrontTarget(self.distribution)),
            )


def website_pf_cloudfront(
    scope: Construct, construct_id: str, config: Config, override_properties: dict = {}, **kwargs
) -> WebsitePfCloudFront:
    """
    Factory function to create the CloudFront distribution for Website-PF stack.

    Args:
        scope: CDK scope
        construct_id: Construct ID
        config: Configuration object
        override_properties: Dictionary of properties to override defaults
        sub_domain: Subdomain to use for custom domain (e.g., 'www')

    """

    cloudfront_distribution = WebsitePfCloudFront(scope, construct_id, config, override_properties, **kwargs)
    return cloudfront_distribution
