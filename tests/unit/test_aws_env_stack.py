import aws_cdk as cdk
import aws_cdk.assertions as assertions

from aws_env.aws_env_stack import AwsEnvStack
from aws_env.tc_cdk_eks_stack import TcCdkEksStack

def test_aws_eks_cluster_created():
    app = cdk.App()
    infraStack = cdk.Stack(app, "AwsEnvStack")
    vpc = cdk.aws_ec2.Vpc(infraStack, "TCVPC")

    eksstack = TcCdkEksStack(app, "TcCdkEksStack", vpc=vpc)
    ekstemplate = assertions.Template.from_stack(eksstack)

    ekstemplate.resource_count_is("Custom::AWSCDK-EKS-Cluster",1)