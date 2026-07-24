from constructs import Construct
from aws_cdk import aws_iam
from config import Config
import utils


class WebsitePfIam():
    """Constructs for IAM roles and policies."""

    role = None
    policy = None

    def __init__(self, scope: Construct, construct_id: str, config: Config, override_properties: dict = {}, additional_policies: list = [], **kwargs):

        # Lambda execution role
        properties = {
            'role_name': f"website-pf-default-role-{config.stage}",
            'assumed_by': aws_iam.ServicePrincipal("lambda.amazonaws.com"),
            'description': "Role for Website-PF Lambda functions",
            'managed_policies': [
                aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                    "service-role/AWSLambdaVPCAccessExecutionRole"
                )
            ]

        }

        policy_statements = [
            aws_iam.PolicyStatement(
                effect=aws_iam.Effect.ALLOW,
                actions=["s3:*"],
                resources=[
                    f"arn:aws:s3:::{config.website_pf_content_bucket_name}",
                    f"arn:aws:s3:::{config.website_pf_content_bucket_name}/*",
                ]
            ),
            aws_iam.PolicyStatement(
                effect=aws_iam.Effect.ALLOW,
                actions=["lambda:InvokeFunction"],
                resources=[
                    f"arn:aws:lambda:{config.region}:{config.account_id}:function:{config.website_pf_loader_lambda_name}"
                ],
            )
        ]
        policy_statements.extend(additional_policies)

        self.policy = aws_iam.Policy(
            scope,
            f"{construct_id}IamPolicy",
            policy_name=properties['role_name'].replace(config.stage, f"policy-{config.stage}"),
            statements=policy_statements
        )

        utils.update_dictionaries(properties, override_properties)
        self.role = aws_iam.Role(
            scope,
            f"{construct_id}IamRole",
            **properties
        )

        self.role.attach_inline_policy(self.policy)
        self.role.without_policy_updates()


def website_pf_api_lambda_iam(scope: Construct, construct_id: str, config: Config, **kwargs) -> WebsitePfIam:
    """Factory function to create IAM role and policies for the main API Lambda function for Website-PF stack."""

    override_properties = {
        'role_name': f"website-pf-api-role-{config.stage}",
        'description': "IAM role for Website-PF API Lambda function"
    }

    additional_policies = [
        aws_iam.PolicyStatement(
            effect=aws_iam.Effect.ALLOW,
            actions=["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents", "logs:TagResource"],
            resources=[f"arn:aws:logs:{config.region}:{config.account_id}:log-group:/aws/lambda/{config.website_pf_api_lambda_name}*"]
        )
    ]

    return WebsitePfIam(scope, construct_id, config, override_properties=override_properties, additional_policies=additional_policies, **kwargs)


def website_pf_loader_lambda_iam(scope: Construct, construct_id: str, config: Config, **kwargs) -> WebsitePfIam:
    """Factory function to create IAM role and policies for the loader Lambda function for Website-PF stack."""

    override_properties = {
        'role_name': f"website-pf-loader-role-{config.stage}",
        'description': "IAM role for Website-PF loader Lambda function"
    }

    additional_policies = [
        aws_iam.PolicyStatement(
            effect=aws_iam.Effect.ALLOW,
            actions=["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents", "logs:TagResource"],
            resources=[f"arn:aws:logs:{config.region}:{config.account_id}:log-group:/aws/lambda/{config.website_pf_loader_lambda_name}*"]
        )
    ]

    return WebsitePfIam(scope, construct_id, config, override_properties=override_properties, additional_policies=additional_policies, **kwargs)
