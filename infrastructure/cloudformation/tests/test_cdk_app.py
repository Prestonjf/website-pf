from aws_cdk.assertions import Template


def test_website_pf_stack(mock_cdk_app, mock_cdk_env, mock_config_ssm):
    from app import CdkStage

    stage = CdkStage(mock_cdk_app, "test", env=mock_cdk_env)

    website_pf_stack = stage.node.try_find_child("WebsitePfStack")
    website_pf_stack_template = Template.from_stack(website_pf_stack)
    website_pf_stack_json = website_pf_stack_template.to_json()

    assert len(website_pf_stack_json['Resources'].items()) > 0
    website_pf_stack_template.resource_count_is("AWS::Lambda::Function", 1)

    website_pf_stack_template.has_resource_properties("AWS::Lambda::Function", {
        "FunctionName": "default-website-pf-test",
    })

    # website_pf_stack_template.has_resource_properties("AWS::Lambda::Function", {
    #     "FunctionName": "website-pf-post-loader-test",
    # })
