from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_eks as eks,
    aws_ec2 as ec2,
    aws_iam as iam
)
from constructs import Construct

class TcCdkEksStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.IVpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        cluster = eks.Cluster(self, "TCCDKEKS",
            version=eks.KubernetesVersion.V1_21,
            cluster_name="TCCDKEKSUSEAST1-01",
            default_capacity=3,
            vpc=vpc,
            default_capacity_instance=ec2.InstanceType("t3.medium")
        )

        admin_user = iam.User.from_user_attributes(self, "eks_test", user_arn="arn:aws:iam::123456789:user/eks_test")
        cluster.aws_auth.add_user_mapping(admin_user, groups=["system:masters"])

        nodegroup = eks.Nodegroup(self, "MyNodegroup",
            cluster=cluster,

            # the properties below are optional
            desired_size=3,
            force_update=False,
            instance_types=[ec2.InstanceType("t3.medium")],
            labels={
                "ManagedNG": "true"
            },
            launch_template_spec=eks.LaunchTemplateSpec(
                disk_size=50,

                # the properties below are optional
                version="version"
            ),
            max_size=5,
            min_size=3,
            nodegroup_name="TCMANAGEDNG-01",
            # node_role="role", (Need an Object ref)
            # release_version="releaseVersion",
            # remote_access=eks.NodegroupRemoteAccess(
            #     ssh_key_name="sshKeyName",

            #     # the properties below are optional
            #     source_security_groups=[security_group]
            # ),
            subnets=ec2.SubnetSelection(
                availability_zones=["availabilityZones"],
                one_per_az=False,
                # subnet_filters=[subnet_filter],
                # subnet_group_name="subnetGroupName",
                # subnet_name="Private", (this didn't work)
                # subnets=[subnet],
                subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT
            ),
            tags={
                "ng_key": "TCMANAGEDNG-01"
            },
            taints=[eks.TaintSpec(
                effect=eks.TaintEffect.NO_SCHEDULE,
                key="NGNAME",
                value="TCMANAGEDNG-01"
            )]
        )