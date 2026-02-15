"""
IAM roles and policies for Website-PF stack.
"""
from aws_cdk import (
    aws_iam as iam,
    core,
)


class WebsitePFIAM(core.Construct):
    """Constructs for IAM roles and policies."""

    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Lambda execution role
        self.lambda_role = iam.Role(
            self,
            "WebsitePFLambdaRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            description="Role for Website-PF Lambda functions",
        )

        # VPC execution policy for Lambda
        self.lambda_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "service-role/AWSLambdaVPCAccessExecutionRole"
            )
        )

        # S3 bucket access
        self.lambda_role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=["s3:*"],
                resources=[
                    f"arn:aws:s3:::website-pf-${{self.node.try_get_context('stage')}}",
                    f"arn:aws:s3:::website-pf-${{self.node.try_get_context('stage')}}/*",
                ],
            )
        )

        # Lambda invocation permissions
        self.lambda_role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=["lambda:InvokeFunction"],
                resources=["*"],
            )
        )

        # CloudWatch Logs
        self.lambda_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "service-role/AWSLambdaBasicExecutionRole"
            )
        )
