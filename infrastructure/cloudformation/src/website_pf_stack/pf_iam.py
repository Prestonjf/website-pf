"""
IAM roles and policies for Website-PF stack.
"""
from constructs import Construct
from aws_cdk import aws_iam



class WebsitePfIAM(Construct):
    """Constructs for IAM roles and policies."""

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Lambda execution role
        self.lambda_role = aws_iam.Role(
            self,
            "WebsitePFLambdaRole",
            assumed_by=aws_iam.ServicePrincipal("lambda.amazonaws.com"),
            description="Role for Website-PF Lambda functions",
        )

        # VPC execution policy for Lambda
        self.lambda_role.add_managed_policy(
            aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                "service-role/AWSLambdaVPCAccessExecutionRole"
            )
        )

        # S3 bucket access
        self.lambda_role.add_to_policy(
            aws_iam.PolicyStatement(
                effect=aws_iam.Effect.ALLOW,
                actions=["s3:*"],
                resources=[
                    f"arn:aws:s3:::website-pf-${{self.node.try_get_context('stage')}}",
                    f"arn:aws:s3:::website-pf-${{self.node.try_get_context('stage')}}/*",
                ],
            )
        )

        # Lambda invocation permissions
        self.lambda_role.add_to_policy(
            aws_iam.PolicyStatement(
                effect=aws_iam.Effect.ALLOW,
                actions=["lambda:InvokeFunction"],
                resources=["*"],
            )
        )

        # CloudWatch Logs
        self.lambda_role.add_managed_policy(
            aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                "service-role/AWSLambdaBasicExecutionRole"
            )
        )
