from constructs import Construct
import aws_cdk as cdk
from aws_cdk import aws_logs
from config import Config
import utils


class WebsitePfLogGroup():
    """Constructs for Cloudwatch LogGroup."""

    log_group = None

    def __init__(self, scope: Construct, construct_id: str, config: Config, override_properties: dict = {}, **kwargs):
        properties = {
            'log_group_name': f"/aws/lambda/website-pf-default-log-group-{config.stage}",
            'retention': aws_logs.RetentionDays.ONE_YEAR,
            'removal_policy': cdk.RemovalPolicy.DESTROY
        }

        utils.update_dictionaries(properties, override_properties)
        self.log_group = aws_logs.LogGroup(
            scope,
            f"{construct_id}LogGroup",
            **properties
        )
