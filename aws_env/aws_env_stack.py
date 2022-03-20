from unicodedata import name
from aws_cdk import (
    # Duration,
    CfnOutput,
    Stack,
    aws_ec2 as ec2,
)
from constructs import Construct

class AwsEnvStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = ec2.Vpc(self, "TCVPC",
            vpc_name="TCVPC",
            cidr="172.16.0.0/16",
            max_azs=2,
            subnet_configuration=[ec2.SubnetConfiguration(cidr_mask=24,subnet_type=ec2.SubnetType.PUBLIC,name="Public"),
            ec2.SubnetConfiguration(cidr_mask=24,subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT,name="Private")],
            nat_gateways=2
        )

        CfnOutput(self, "Output", value=self.vpc.vpc_id)
        
    @property
    def main_vpc(self) -> ec2.IVpc:
        return self.vpc