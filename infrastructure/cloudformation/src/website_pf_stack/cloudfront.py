"""
CloudFront distribution for Website-PF stack.
"""
from aws_cdk import (
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_s3 as s3,
    aws_iam as iam,
    aws_certificatemanager as acm,
    core,
)


class WebsitePFCloudFront(core.Construct):
    """CloudFront distribution for Website-PF."""

    def __init__(
        self,
        scope: core.Construct,
        id: str,
        stage: str,
        version: str,
        acm_config: dict,
        waf_config: dict,
        **kwargs,
    ):
        super().__init__(scope, id, **kwargs)

        # S3 bucket for website
        self.bucket = s3.Bucket(
            self,
            "WebsitePFBucket",
            bucket_name=f"website-pf-{stage}",
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED,
        )

        # CloudFront Origin Access Identity
        oai = cloudfront.OriginAccessIdentity(
            self,
            "WebsitePFOAI",
            comment=f"website-pf-{stage}-access-identity",
        )

        # Grant OAI read access to bucket
        self.bucket.grant_read(oai)

        # Cache policy
        cache_policy = cloudfront.CachePolicy(
            self,
            "WebsitePFCachePolicy",
            cache_policy_name=f"website-pf-{stage}-cache-policy",
            default_ttl=core.Duration.days(1),
            max_ttl=core.Duration.days(365),
            min_ttl=core.Duration.seconds(1),
            enable_accept_encoding_brotli=True,
            enable_accept_encoding_gzip=True,
        )

        # Origin request policy
        origin_request_policy = cloudfront.OriginRequestPolicy(
            self,
            "WebsitePFOriginRequestPolicy",
            origin_request_policy_name=f"website-pf-{stage}-origin-request-policy",
            header_behavior=cloudfront.OriginRequestHeaderBehavior.whitelist(
                "origin", "access-control-request-headers", "access-control-request-method"
            ),
        )

        # CloudFront distribution
        self.distribution = cloudfront.Distribution(
            self,
            "WebsitePFDistribution",
            default_root_object=f"site/{version}/index.html",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(self.bucket, origin_access_identity=oai),
                cache_policy=cache_policy,
                origin_request_policy=origin_request_policy,
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                response_headers_policy=cloudfront.ResponseHeadersPolicy.from_response_headers_policy_id(
                    "5cc3b908-e619-4b99-88e5-2cf7f45965bd"
                ),
            ),
            error_responses=[
                cloudfront.ErrorResponse(
                    http_status=403,
                    response_http_status=200,
                    response_page_path=f"/site/{version}/index.html",
                ),
                cloudfront.ErrorResponse(
                    http_status=404,
                    response_http_status=200,
                    response_page_path=f"/site/{version}/index.html",
                ),
            ],
            domain_names=["prestonfrazier.net", "www.prestonfrazier.net"],
            certificate=self._get_certificate(acm_config),
            web_acl_id=waf_config.get("arn") if waf_config else None,
            price_class=cloudfront.PriceClass.PRICE_CLASS_100,
            comment=f"Website-PF serverless distribution for webapp in s3 bucket",
        )

        # Add S3 bucket policy to allow read access from CloudFront and Lambda
        self.bucket.add_to_resource_policy(
            iam.PolicyStatement(
                sid="OAIReadGetObjects",
                effect=iam.Effect.ALLOW,
                principals=[oai],
                actions=["s3:GetObject"],
                resources=[f"{self.bucket.bucket_arn}/*"],
            )
        )

    def _get_certificate(self, acm_config: dict):
        """Get ACM certificate from config."""
        if acm_config and "arn" in acm_config:
            # Import existing certificate
            arn = acm_config["arn"]
            # Use the ARN to reference existing certificate
            return cloudfront.Certificate.from_certificate_arn(
                self,
                "WebsitePFCertificate",
                certificate_arn=arn,
            )
        return None
