import aws_cdk as core
import aws_cdk.assertions as assertions

from aws_env.aws_env_stack import AwsEnvStack
from aws_env.tc_cdk_eks_stack import TcCdkEksStack

# example tests. To run these tests, uncomment this file along with the example
# resource in aws_env/aws_env_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = AwsEnvStack(app, "aws-env")
    template = assertions.Template.from_stack(stack)
    
    eksstack = TcCdkEksStack(app, "aws-env")
    ekstemplate = assertions.Template.from_stack(eksstack)

    ekstemplate.resource_count_is("AWS::EKS::Cluster",1)
#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
