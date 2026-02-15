"""
Lambda functions and layers for Website-PF stack.
"""
import os
from aws_cdk import (
    aws_lambda as lambda_,
    aws_lambda_python as lambda_python,
    aws_iam as iam,
    core,
)


class WebsitePFLambdaLayer(core.Construct):
    """Lambda layer with shared dependencies."""

    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        backend_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "..",
            "backend",
            "website-pf",
        )

        # Create Lambda layer from backend dependencies
        self.layer = lambda_python.PythonLayerVersion(
            self,
            "WebsitePFDependencies",
            entry=backend_path,
            compatible_runtimes=[lambda_.Runtime.PYTHON_3_13],
            description="Lambda Layer for Website-PF application dependencies",
        )


class WebsitePFLambdaFunctions(core.Construct):
    """Lambda functions for Website-PF stack."""

    def __init__(
        self,
        scope: core.Construct,
        id: str,
        lambda_role: iam.Role,
        layer: lambda_python.PythonLayerVersion,
        stage: str,
        environment_vars: dict,
        vpc_config: dict,
        **kwargs,
    ):
        super().__init__(scope, id, **kwargs)

        backend_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "..",
            "backend",
            "website-pf",
        )

        # Website PF API Lambda function
        self.website_pf_api = lambda_python.PythonFunction(
            self,
            "WebsitePFAPI",
            entry=os.path.join(backend_path, "src"),
            index="website_pf_api/app.py",
            handler="lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_13,
            function_name=f"website-pf-{stage}",
            description="Website-PF backend for querying and retrieving post information.",
            memory_size=256,
            timeout=core.Duration.seconds(10),
            role=lambda_role,
            layers=[layer],
            environment=environment_vars,
            vpc_subnets={"subnets": [vpc_config.get("subnet")]},
            security_groups=[vpc_config.get("security_group")],
            allow_public_subnet=True,
        )

        # Website PF Post Loader Lambda function
        self.website_pf_post_loader = lambda_python.PythonFunction(
            self,
            "WebsitePFPostLoader",
            entry=os.path.join(backend_path, "src"),
            index="website_pf_post_loader/app.py",
            handler="lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_13,
            function_name=f"website-pf-post-loader-{stage}",
            description="Website-PF loader for new and existing posts.",
            memory_size=256,
            timeout=core.Duration.seconds(30),
            role=lambda_role,
            layers=[layer],
            environment={**environment_vars, "FEATURED_POSTS": "about,portfolio"},
            vpc_subnets={"subnets": [vpc_config.get("subnet")]},
            security_groups=[vpc_config.get("security_group")],
            allow_public_subnet=True,
        )
