#!/usr/bin/env python3
"""
Main CDK Application for Website-PF Infrastructure.

This application synthesizes the CloudFormation template for the Website-PF
lambda functions, S3 bucket, CloudFront distribution, and related AWS resources.

Usage:
    python app.py          # Synthesize CDK
    cdk deploy             # Deploy to AWS
    cdk deploy --stage dev # Deploy to dev environment
"""
import aws_cdk as cdk
from aws_cdk import App, Stage
from src import utils
from src.config import Config
from src.website_pf_stack import WebsitePfStack

logger = utils.setup_logging()


class CdkStage(Stage):
    """CDK Stage for Website-PF stack."""

    def __init__(self, scope: cdk.Construct, stage_id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Get configuration
        config = Config(stage_id, kwargs['env'], app_version="1.0.0", project_name="website-pf")

        # Add tags
        cdk.Tags.of(self).add("Application", "website-pf")
        cdk.Tags.of(self).add("Environment", config.stage)
        cdk.Tags.of(self).add("Version", config.version)
        cdk.Tags.of(self).add("ManagedBy", "CDK")

        # Create stack
        WebsitePfStack(
            self,
            "WebsitePfStack",
            config,
            stack_name=config.website_pf_stack_name,
            description=f"Website-PF Infrastructure Stack ({config.stage})",
            synthesizer=utils.get_stack_synthesizer(config, config.website_pf_stack_name)
        )


def package_project_assets():
    """Package project assets for deployment."""
    pass


def main():
    """Main entry point for CDK application."""
    logger.info("Starting CDK application synthesis...")
    app = App()

    stage_name, env = utils.get_stage_environment()

    if stage_name and env:
        logger.info(f"Deploying stage '{stage_name}' to environment '{env}'")
        package_project_assets()
        CdkStage(app, stage_name, env=env)
        app.synth()
    else:
        logger.info("No stage or environment found.")

    logger.info("Finished CDK application synthesis.")


if __name__ == "__main__":
    main()
