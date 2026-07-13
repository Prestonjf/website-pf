#!/usr/bin/env python3
"""
Main CDK Application for Website-PF Infrastructure.

This application synthesizes the CloudFormation template for the Website-PF
lambda functions, S3 bucket, CloudFront distribution, and related AWS resources.
"""
from constructs import Construct
import aws_cdk as cdk
from aws_cdk import App, Stage
import utils
from config import Config
from website_pf_stack.pf_stack import WebsitePfStack

logger = utils.setup_logging()


class CdkStage(Stage):
    """CDK Stage for Website-PF stack."""

    def __init__(self, scope: Construct, stage_id: str, **kwargs):
        super().__init__(scope, stage_id, **kwargs)

        # Get configuration
        config = Config(stage_id, kwargs['env'], app_version="1.0.0", project_name="website-pf")

        # Add tags
        cdk.Tags.of(self).add("Application", config.project_name)
        cdk.Tags.of(self).add("Stage", config.stage)
        cdk.Tags.of(self).add("Customer", config.customer)
        cdk.Tags.of(self).add("Environment", config.environment)
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


def main():
    """Main entry point for CDK application."""
    logger.info("Starting CDK application synthesis...")
    app = App()

    stage_name, env = utils.get_stage_environment(app)

    if stage_name and env:
        logger.info(f"Deploying stage '{stage_name}' to environment '{env}'")
        CdkStage(app, stage_name, env=env)
        app.synth()
    else:
        logger.info("No stage or environment found.")

    logger.info("Finished CDK application synthesis.")


if __name__ == "__main__":
    main()
